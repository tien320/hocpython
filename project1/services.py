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
if __name__ == "__main__":
    p_repo = ProductRepository()
    o_repo = OrderRepository()
    service = OrderService(product_repo = p_repo,order_repo = o_repo)
    sp = p_repo.create("chuột ko dây",500000,5)
    print("sản phẩm",sp)
    don_hang = service.place_order(product_id = sp.id,quantity =2)
    print("mua hàng thành công",don_hang)
    don_hang_loi = service.place_order(product_id = sp.id, quantity = 10)
    print("mua qua so luong",don_hang_loi)
        