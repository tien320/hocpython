from models.mathang import MatHang
from models.dodientu import DienTu
from models.dotuoisong import TuoiSong
def main():
    try:
        print("tạo lỗi")
        vat_pham_loi = MatHang("vat pham la",5000,1)
    except TypeError as t:
        print(t)
    kho_hang =[
        DienTu("tv",15000000,5,24),
        TuoiSong("thit bo",259000,10,3)
    ]
    for mat_hang in kho_hang:
        thue = mat_hang.tinh_thue()
        thong_tin = mat_hang.hien_thi_thong_tin()
        print(f"{thong_tin} và Thuế: {thue}")
if __name__ == "__main__":
    main()