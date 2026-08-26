from repository import ProductRepository
from repository import OrderRepository
class OrderService:
    def __init__(self,product_repo: ProductRepository,order_repo: OrderRepository):
        self.product_repo = product_repo
        self.order_repo = order_repo
    def place_order(self,product_id:int,quantity:int):
        product = self.product_repo.get_by_id(product_id)
        if not product: return None
        if not product.is_available(quantity) : return None
        total_price = product.price * quantity
        product.reduce_stock(quantity)
        self.product_repo.update_stock(new_stock=product.stock,product_id=product_id)
        new_order = self.order_repo.create(product_id=product_id,quantity=quantity,total_price=total_price,status="COMPLETED")
        return new_order