from database import DatabaseConnection
from model import Product
from model import Order
class ProductRepository:
    def __init__(self,db_factory=DatabaseConnection):
        self.db_factory = db_factory
    def create(self, name:str, price:float, stock:int):
        with self.db_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "insert into products(name,price,stock) values (?,?,?)",(name,price,stock)
            )
            new_id = cursor.lastrowid
            return Product(id=new_id,name=name,price=price,stock=stock)
    def get_by_id(self,product_id:int):
        with self.db_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "select id,name,price,stock from products where id =?",(product_id,)
            )
            row = cursor.fetchone()
            if row:
                return Product(id=row["id"],name=row["name"],price=row["price"],stock=row["stock"])
            return None
    def update_stock(self,new_stock:int,product_id:int):
        with self.db_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "update products set stock = ? where id = ?",(new_stock,product_id)
            )
            return cursor.rowcount>0
class OrderRepository:
    def __init__(self,db_factory = DatabaseConnection):
        self.db_factory = db_factory
    def create(self,product_id:int,quantity:int,total_price:float,status:str="PENDING"):
        with self.db_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "insert into orders(product_id,quantity,total_price,status) values (?,?,?,?)",
                (product_id,quantity,total_price,status)
            )
            new_id = cursor.lastrowid
            return Order(id=new_id,product_id=product_id,quantity=quantity,total_price=total_price,status=status)
        