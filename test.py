import pandas as pd
import oracledb
from sqlalchemy import create_engine, String,Numeric
import io
users_csv = """user_id,user_name,password,email,address
I001,Le Tien,tien1344,tien@gmail.com,Ha Noi
I002,Le Dang,dang2334,dang@gamil.com,Ha Noi
I003,Nguyen Anh,anh1222,anh@gmail.com,Ha Noi"""
def read_csv():
    try:
        df = pd.read_csv(
            io.StringIO(users_csv),
            sep= ','
        ).reset_index()
        print("đã đọc")
        print(df.info())
        return df
    except Exception as e:
        print(e)
def save_to_oracle(df):
    if df is None: return None
    try:
        engine = create_engine("oracle+oracledb://OLIST:123456@localhost:1521/?service_name=XEPDB1")
        df.to_sql(name = 'userss', con = engine, if_exists = 'replace', index = False)
        print("đã save")
        return df
    except Exception as e:
        print(e)
if __name__ == "__main__":
    df = read_csv()
    save_to_oracle(df)
