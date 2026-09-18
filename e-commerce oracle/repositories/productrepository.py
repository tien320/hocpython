from models.products import Product
from core.database import Database

class ProductRepository:
    def __init__(self, db: Database | None = None):
        self.db = db if db is not None else Database()
    def list_all(self):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("select * from products")
                col_names = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()
                return[self._map_row_to_product(dict(zip(col_names,row))) for row in rows]
    def _map_row_to_product(self, data: dict):
           return Product(
              product_id = data["product_id"],
              name = data["name"],
              price = data["price"],
              stock = data["stock"],
              created_at = data["created_at"]
           )
    def add(self, product: Product):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("insert into products(product_id,name,price,stock,created_at) values(:product_id, :name, :price, :stock, :created_at)",{
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "stock": product.stock,
                    "created_at": product.created_at   
                })
                conn.commit()
                return cursor.rowcount > 0
    def find_by_id(self,product_id: int):
           with self.db.get_connection() as conn:
              with conn.cursor() as cursor:
                 cursor.execute("select * from products where product_id = :id", id = product_id)
                 row = cursor.fetchone()
                 if not row: return None
                 col_names = [col[0].lower() for col in cursor.description]
                 return self._map_row_to_product(dict(zip(col_names,row)))
    def update(self,product_id: int,product: Product):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("update products set name = :name, price = :price, stock = :stock, created_at = :created_at where product_id = :product_id",
                    {
                       "name": product.name,
                       "price": product.price,
                       "stock": product.stock,
                       "created_at": product.created_at,
                       "product_id": product_id
                 })
                conn.commit()
                return cursor.rowcount > 0
    def delete(self, product_id: int):
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("delete from products where product_id = :product_id",product_id=product_id)
                conn.commit()
                return cursor.rowcount > 0
                        
        