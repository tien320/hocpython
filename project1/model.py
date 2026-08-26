class Product:
    def __init__(self,id:int, name: str, price : float, stock : int):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
    def is_available(self,quantity):
        if self.stock >= quantity :
            return True
        else:
            return False
    def reduce_stock(self,quantity):
        if self.is_available(quantity):
            self.stock= self.stock - quantity
            return True
        return False
    def __repr__(self):
        return f"Product(id={self.id},name={self.name},price={self.price},stock={self.stock})"
class Order:
    def __init__(self,id : int, product_id:int, quantity:int, total_price:float,status:str = "PENDING"):
        self.id = id
        self.product_id = product_id 
        self.quantity = quantity
        self.total_price = total_price
        self.status = status
    def complete(self):
        self.status = "COMPLETED"
    def cancel(self):
        self.status = "CANCELLED"
    def __repr__(self):
        return f"Order(id={self.id},product_id={self.product_id},quantity={self.quantity},total={self.total_price},status={self.status})"