from pathlib import Path
import oracledb
import pandas as pd
from sqlalchemy import DateTime, Integer, Numeric, String, Text, create_engine
DATE_CONFIG = {
    'orders': [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
    ],
    'order_items': ['shipping_limit_date'],
    'order_reviews': ['review_creation_date', 'review_answer_timestamp'],
}
DTYPES_CONFIG = {
    'customers': {
        'customer_id': String(50),
        'customer_unique_id': String(50),
        'customer_zip_code_prefix': Integer(),
        'customer_city': String(100),
        'customer_state': String(5),
    },
    'sellers': {
        'seller_id': String(50),
        'seller_zip_code_prefix': Integer(),
        'seller_city': String(100),
        'seller_state': String(5),
    },
    'products': {
        'product_id': String(50),
        'product_category_name': String(100),
        'product_name_lenght': Integer(),
        'product_description_lenght': Integer(),
        'product_photos_qty': Integer(),
        'product_weight_g': Numeric(10, 2),
        'product_length_cm': Numeric(10, 2),
        'product_height_cm': Numeric(10, 2),
        'product_width_cm': Numeric(10, 2),
    },
    'geolocation': {
        'geolocation_zip_code_prefix': Integer(),
        'geolocation_lat': Numeric(12, 8),
        'geolocation_lng': Numeric(12, 8),
        'geolocation_city': String(100),
        'geolocation_state': String(5),
    },
    'orders': {
        'order_id': String(50),
        'customer_id': String(50),
        'order_status': String(30),
        'order_purchase_timestamp': DateTime(),
        'order_approved_at': DateTime(),
        'order_delivered_carrier_date': DateTime(),
        'order_delivered_customer_date': DateTime(),
        'order_estimated_delivery_date': DateTime(),
    },
    'order_items': {
        'order_id': String(50),
        'order_item_id': Integer(),
        'product_id': String(50),
        'seller_id': String(50),
        'shipping_limit_date': DateTime(),
        'price': Numeric(12, 2),
        'freight_value': Numeric(12, 2),
    },
    'order_payments': {
        'order_id': String(50),
        'payment_sequential': Integer(),
        'payment_type': String(30),
        'payment_installments': Integer(),
        'payment_value': Numeric(12, 2),
    },
    'order_reviews': {
        'review_id': String(50),
        'order_id': String(50),
        'review_score': Integer(),
        'review_comment_title': String(255),
        'review_comment_message': Text(),
        'review_creation_date': DateTime(),
        'review_answer_timestamp': DateTime(),
    },
}

if __name__ == '__main__':
  BASE_DIR = Path(__file__).resolve().parent
  DATA_DIR = BASE_DIR / 'olist'

  engine = create_engine(
      'oracle+oracledb://OLIST:123456@localhost:1521/?service_name=XEPDB1'
  )

  if not DATA_DIR.exists():
    print('ko có')
  else:
    for file_path in DATA_DIR.glob('olist_*.csv'):
      table_name = file_path.stem.replace('olist_', '').replace(
          '_dataset', ''
      )
      parse_dates = DATE_CONFIG.get(table_name, False)

      try:
        df = pd.read_csv(file_path, parse_dates=parse_dates, low_memory=False)
        print('đã đọc')
        dtype_map = DTYPES_CONFIG.get(table_name, None)
        with engine.begin() as conn:
          df.to_sql(
              name=table_name,
              con=conn,
              if_exists='replace',
              index=False,
              dtype=dtype_map,
              chunksize=5000,
          )
        print('đã save')
      except Exception as e:
        print(e)