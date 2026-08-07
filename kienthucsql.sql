SELECT company_name, country, credit_limit
FROM customers
WHERE country = 'Germany'             -- Lấy người ở Germany
  AND credit_limit BETWEEN 1000 AND 3000 -- Hạn mức từ 1000 đến 3000
  AND status IN ('ACTIVE', 'PENDING');  -- Trạng thái thuộc 1 trong 2 loại này
  
 -- Lấy danh sách quốc gia không trùng lặp
SELECT DISTINCT country AS quoc_gia 
FROM customers;

-- Sắp xếp giảm dần và lấy TOP 3 người giàu nhất
SELECT company_name AS ten_cong_ty, credit_limit AS tien
FROM customers
ORDER BY credit_limit DESC
OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY; -- Tương đương LIMIT 3 trong MySQL

SELECT 
    -- Chuyển Số thành Chữ có dấu $ và dấu phẩy hàng nghìn
    TO_CHAR(1500.5, '$9,999.00') AS tien_dep, -- Trả về "$1,500.50"
    
    -- Chuyển Chữ thành Ngày chuẩn để lưu vào máy
    TO_DATE('2026-08-07', 'YYYY-MM-DD') AS ngay_chuan
FROM DUAL; -- DUAL là bảng ảo của Oracle dùng để test nhanh

SELECT 
    LOWER('CHỮ HOA')            AS thanh_chu_thuong, -- 'chữ hoa'
    UPPER('chữ thường')          AS thanh_chu_hoa,    -- 'CHỮ THƯỜNG'
    TRIM('   dư khoảng trắng   ') AS mat_khoang_trang,
    
    -- Cắt chữ: SUBSTR(Chuỗi, Vị trí bắt đầu, Độ dài)
    SUBSTR('CHINOOK', 1, 3)     AS lay_3_ky_tu_dau,  -- 'CHI'
    
    -- Ghép chữ: Dùng dấu ||
    'Xin chào ' || 'Viet Nam'    AS ghep_chu          -- 'Xin chào Viet Nam'
FROM DUAL;

SELECT 
    SYSDATE AS ngay_gio_hien_tai,
    
    -- TRUNC: Chặt bỏ giờ phút giây, chỉ lấy mốc đầu ngày/đầu tháng
    TRUNC(SYSDATE, 'MM') AS ngay_dau_tien_cua_thang,
    
    -- EXTRACT: "Rút" riêng Năm hoặc Tháng ra thành số
    EXTRACT(YEAR FROM SYSDATE)  AS nam_hien_tai,
    EXTRACT(MONTH FROM SYSDATE) AS thang_hien_tai
FROM DUAL;

SELECT 
    ROUND(125.678, 2) AS lam_tron_2_so, -- 125.68
    CEIL(125.1)       AS lam_tron_LEN, -- 126
    FLOOR(125.9)      AS lam_tron_XUONG, -- 125
    
    -- Minh họa lỗi với NULL:
    100 + NULL        AS ket_qua_null -- Trả về NULL!
FROM DUAL;

SELECT 
    company_name,
    
    -- Nếu chưa có tên người liên hệ (NULL) -> Thay bằng chữ 'Chưa cập nhật'
    COALESCE(contact_name, 'Chưa cập nhật') AS ten_an_toan,
    
    -- Tính toán an toàn: Nếu credit_limit bị NULL -> coi như là 0 để tính
    COALESCE(credit_limit, 0) + 100 AS tien_sau_khi_cong,
    
    -- Tránh lỗi chia cho 0: Nếu mau_so = 0 thì biến thành NULL
    100 / NULLIF(0, 0) AS phan_song_an_toan -- Trả về NULL chứ không văng lỗi Crash code!
FROM customers;
SELECT 
    bảng_A.tên_cột_1,
    bảng_B.tên_cột_2
FROM bảng_A
INNER JOIN bảng_B 
    ON bảng_A.khóa_ngoại = bảng_B.khóa_chính;
 SELECT * 
FROM HocSinh A
LEFT JOIN LopHoc B ON A.ID = B.ID_HocSinh;
SELECT * 
FROM HocSinh A
RIGHT JOIN LopHoc B ON A.ID = B.ID_HocSinh;
SELECT * 
FROM HocSinh A
FULL OUTER JOIN LopHoc B ON A.ID = B.ID_HocSinh;
SELECT 
    E.ID AS NhanVienID,
    E.Ten AS TenNhanVien,
    M.Ten AS TenQuanLy
FROM NhanVien E
LEFT JOIN NhanVien M ON E.QuanLyID = M.ID;
SELECT     PhongBanID, COUNT(*) AS SoNV, AVG(Luong) AS LuongTB
FROM       NhanVien
WHERE      TrangThai = 'Active'     -- 1. Lọc dòng thô trước
GROUP BY   PhongBanID              -- 2. Gom nhóm theo phòng
HAVING     COUNT(*) >= 5            -- 3. Lọc nhóm có từ 5 NV trở lên
ORDER BY   LuongTB DESC;            -- 4. Sắp xếp kết quả cuối cùng

