import csv
import json

raw_logs_json = '''[
    {"id": "TX101", "user": "An", "items": ["Sách", "Bút"], "total": 150000, "status": "success"},
    {"id": "TX102", "user": "Bình", "items": ["Tai nghe"], "total": 500000, "status": "failed"},
    {"id": "TX103", "user": "An", "items": ["Vở", "Bao thư", "Thước"], "total": 85000, "status": "success"}
]'''
logs = json.loads(raw_logs_json)
giao_dich_thanh_cong =[]
for log in logs:
    if log['status'] == "success":
       items_str = ",".join(log['items']) 
       giao_dich_thanh_cong.append({
           'id' : log['id'],
           'user' : log['user'],
           'items' : items_str,
           'total' : log['total'],
           'status' : log['status']
       })
with open('thanh_cong.csv',mode='w',newline='',encoding='utf-8') as f_csv:
    field_name = ['id','user','items','total','status']
    writer = csv.DictWriter(f_csv,fieldnames=field_name)
    writer.writeheader()
    writer.writerows(giao_dich_thanh_cong)
print('thanh cong')
