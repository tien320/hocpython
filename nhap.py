import pandas as pd
import oracledb
from sqlalchemy import create_engine, String, Date,Numeric
import io
transactions_csv = """tran_id|cust_id|tran_date|amount|channel
TX1001|C01|2026-08-10|500000|App
TX1002|C02|2026-08-11|INVALID|Web
TX1003|C01|2026-08-11|1200000|App
TX1004|C03|2026-08-12|750000|POS
TX1005|C04|2026-08-12|NULL|App"""
def read_file():
    df_trans = pd.read_csv(
        io.StringIO(transactions_csv),
        sep = "|",
        usecols=[
            "tran_id",
            "cust_id",
            "tran_date",
            "amount",
            "channel"
        ],
        parse_dates= ["tran_date"],
        na_values= ["INVALID","NULL"]
    )
    print("đã đọc")
    return df_trans
def save_to_oracle(df):
    oracle_uri = "oracle+oracledb://OLIST:123456@localhost:1521/?service_name=XEPDB1"
    try:
        engine = create_engine(oracle_uri)
        dtype_mapping = {
            "tran_id" : String(50),
            "cust_id" : String(50),
            "tran_date" : Date(),
            "amount" : Numeric(15,2),
            "channel" : String(50)
        }
        df.to_sql(
           'df_trans',
            con = engine,
            if_exists = 'replace',
            index = False,
            dtype=dtype_mapping
        )
        print("đã save")
    except Exception as e:
        # In ra lỗi chi tiết nếu kết nối DB thất bại
        print(f"\nlỗi.chi tiết:\n{e}\n")
if __name__ == "__main__":
    df_trans = read_file()
    save_to_oracle(df_trans)

