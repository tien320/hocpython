users = [
    {"user_id": 1, "name": "An"},
    {"user_id": 2, "name": "Bình"},
    {"user_id": 3, "name": "Cường"}
]

orders = [
    {"order_id": 101, "user_id": 1, "total": 500000},
    {"order_id": 102, "user_id": 2, "total": 300000},
    {"order_id": 103, "user_id": 1, "total": 150000}
]
user_map = {user['user_id']: user['name'] for user in users}
order_details = []
for order in orders:
    if order['user_id'] in user_map:
        order_details.append({
            "order_id": order['order_id'],
            "user_name": user_map[order['user_id']],
            "total": order['total']
        })
import pprint
pprint.pprint(order_details)    