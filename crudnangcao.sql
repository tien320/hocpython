-- =============================================================================
-- 1. VIEWS (Tầng Read / Abstraction Layer)
-- =============================================================================

-- 1.1. Standard Reporting View (Kết hợp Window function & Phân nhóm)
CREATE OR REPLACE VIEW v_active_users_summary AS
SELECT 
    user_id,
    username,
    email,
    balance,
    tier,
    status,
    CASE 
        WHEN balance >= 500 THEN 'VIP'
        WHEN balance >= 200 THEN 'PREMIUM'
        ELSE 'STANDARD'
    END AS computed_tier,
    SUM(balance) OVER () AS total_system_balance,
    DENSE_RANK() OVER (ORDER BY balance DESC) AS balance_rank
FROM users
WHERE status = 'ACTIVE';

-- 1.2. View có kiểm tra bảo vệ toàn vẹn dữ liệu (WITH CHECK OPTION)
CREATE OR REPLACE VIEW v_standard_users AS
SELECT user_id, username, email, balance, status
FROM users
WHERE status = 'ACTIVE'
WITH CHECK OPTION CONSTRAINT chk_active_only;


-- =============================================================================
-- 2. STANDALONE PROCEDURES (Tầng Cập nhật / Xử lý nghiệp vụ riêng lẻ)
-- =============================================================================

-- 2.1. Procedure Update Balance (Xử lý giao dịch nạp/rút kèm Transaction Control)
CREATE OR REPLACE PROCEDURE sp_update_user_balance (
    p_user_id IN  users.user_id%TYPE,
    p_amount  IN  NUMBER,
    p_status  OUT VARCHAR2
) 
AS
    v_current_balance users.balance%TYPE;
BEGIN
    -- Khóa bản ghi (Pessimistic Locking) tránh Race Condition
    SELECT balance 
    INTO v_current_balance
    FROM users
    WHERE user_id = p_user_id
    FOR UPDATE;

    -- Kiểm tra số dư nếu là giao dịch trừ tiền
    IF (v_current_balance + p_amount) < 0 THEN
        p_status := 'FAILED: INSUFFICIENT_FUNDS';
        ROLLBACK;
        RETURN;
    END IF;

    -- Cập nhật số dư
    UPDATE users
    SET balance = balance + p_amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE user_id = p_user_id;

    COMMIT;
    p_status := 'SUCCESS';

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_status := 'FAILED: USER_NOT_FOUND';
        ROLLBACK;
    WHEN OTHERS THEN
        p_status := 'FAILED: ' || SQLERRM;
        ROLLBACK;
END sp_update_user_balance;
/


-- =============================================================================
-- 3. PACKAGE SPECIFICATION (Khai báo giao diện / Header của Package)
-- =============================================================================
CREATE OR REPLACE PACKAGE pkg_user_management AS

    -- Kiểu dữ liệu con trỏ trả về cho Client/Backend (SYS_REFCURSOR)
    TYPE t_cursor IS REF CURSOR;

    -- C - CREATE: Thêm mới người dùng, trả về ID vừa tạo
    PROCEDURE create_user (
        p_username  IN  users.username%TYPE,
        p_email     IN  users.email%TYPE,
        p_balance   IN  users.balance%TYPE DEFAULT 0,
        o_user_id   OUT users.user_id%TYPE
    );

    -- R - READ: Lấy thông tin user bằng Ref Cursor
    PROCEDURE get_user_by_id (
        p_user_id IN  users.user_id%TYPE,
        o_cursor  OUT t_cursor
    );

    -- R - READ: Function tính toán nhanh chiết khấu theo tier
    FUNCTION calculate_discount (
        p_user_id IN users.user_id%TYPE
    ) RETURN NUMBER;

    -- U - UPDATE: Upsert dữ liệu (MERGE)
    PROCEDURE upsert_user (
        p_user_id   IN users.user_id%TYPE,
        p_username  IN users.username%TYPE,
        p_email     IN users.email%TYPE,
        p_balance   IN users.balance%TYPE,
        p_status    IN users.status%TYPE
    );

    -- D - DELETE: Soft delete người dùng
    PROCEDURE soft_delete_user (
        p_user_id IN users.user_id%TYPE
    );

END pkg_user_management;
/


-- =============================================================================
-- 4. PACKAGE BODY (Cài đặt chi tiết logic CRUD)
-- =============================================================================
CREATE OR REPLACE PACKAGE BODY pkg_user_management AS

    -- C - CREATE Implementation
    PROCEDURE create_user (
        p_username  IN  users.username%TYPE,
        p_email     IN  users.email%TYPE,
        p_balance   IN  users.balance%TYPE DEFAULT 0,
        o_user_id   OUT users.user_id%TYPE
    ) AS
    BEGIN
        INSERT INTO users (username, email, balance, status)
        VALUES (p_username, p_email, p_balance, 'ACTIVE')
        RETURNING user_id INTO o_user_id;

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(-20001, 'Lỗi khi tạo User: ' || SQLERRM);
    END create_user;

    -- R - READ Implementation (Dynamic Cursor)
    PROCEDURE get_user_by_id (
        p_user_id IN  users.user_id%TYPE,
        o_cursor  OUT t_cursor
    ) AS
    BEGIN
        OPEN o_cursor FOR
            SELECT user_id, username, email, balance, tier, status, created_at
            FROM users
            WHERE user_id = p_user_id;
    END get_user_by_id;

    -- R - Function Implementation
    FUNCTION calculate_discount (
        p_user_id IN users.user_id%TYPE
    ) RETURN NUMBER AS
        v_balance NUMBER := 0;
        v_discount NUMBER := 0;
    BEGIN
        SELECT balance INTO v_balance FROM users WHERE user_id = p_user_id;
        
        IF v_balance >= 500 THEN
            v_discount := 0.15; -- 15%
        ELSIF v_balance >= 200 THEN
            v_discount := 0.05; -- 5%
        ELSE
            v_discount := 0.00;
        END IF;

        RETURN v_discount;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 0.00;
    END calculate_discount;

    -- U - UPDATE (UPSERT via MERGE)
    PROCEDURE upsert_user (
        p_user_id   IN users.user_id%TYPE,
        p_username  IN users.username%TYPE,
        p_email     IN users.email%TYPE,
        p_balance   IN users.balance%TYPE,
        p_status    IN users.status%TYPE
    ) AS
    BEGIN
        MERGE INTO users t
        USING (SELECT p_user_id AS uid FROM dual) s
        ON (t.user_id = s.uid)
        WHEN MATCHED THEN
            UPDATE SET 
                t.username   = p_username,
                t.email      = p_email,
                t.balance    = p_balance,
                t.status     = p_status,
                t.updated_at = CURRENT_TIMESTAMP
        WHEN NOT MATCHED THEN
            INSERT (username, email, balance, status)
            VALUES (p_username, p_email, p_balance, p_status);

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END upsert_user;

    -- D - DELETE Implementation (Soft Delete)
    PROCEDURE soft_delete_user (
        p_user_id IN users.user_id%TYPE
    ) AS
    BEGIN
        UPDATE users
        SET status = 'DELETED',
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = p_user_id;

        IF SQL%ROWCOUNT = 0 THEN
            RAISE_APPLICATION_ERROR(-20002, 'User ID không tồn tại để xóa.');
        END IF;

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END soft_delete_user;

END pkg_user_management;
/


-- =============================================================================
-- 5. TEST & EXECUTION (Mẫu lệnh thực thi kiểm thử)
-- =============================================================================

-- Gọi Create từ Package
DECLARE
    v_id NUMBER;
BEGIN
    pkg_user_management.create_user('john_doe', 'john@test.com', 350.00, v_id);
    DBMS_OUTPUT.PUT_LINE('New User Created with ID: ' || v_id);
END;
/

-- Gọi Procedure cập nhật số dư độc lập
DECLARE
    v_msg VARCHAR2(100);
BEGIN
    sp_update_user_balance(p_user_id => 1, p_amount => -50.00, p_status => v_msg);
    DBMS_OUTPUT.PUT_LINE('Result: ' || v_msg);
END;
/

-- Truy vấn từ View đã tạo
SELECT * FROM v_active_users_summary;