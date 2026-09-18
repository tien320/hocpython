from core.database import Database
from datetime import date
from models.orders import Order

class OrderRepository:
    def __init__(self, db: str = Database() | None = None):
        self.db = db if db is not None else Database()
    def _map_row_to_order(self, data: dict):
        return Order(
            order_id = data["order_id"],
            customer_id = data["customer_id"],
            total_amount = data["total_amount"],
            status = data["status"],
            created_at = data["created_at"]
        )
    def list_all():
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("select * from orders")
                col_names = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()
                return[self._map_row_to_order(dict(zip(col_names,row))) for row in rows]

        