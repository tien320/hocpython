from abc import ABC,abstractmethod
class MatHang(ABC):
    def __init__(self,name:str,price:float,stock:int):
        self.__stock = stock if stock >= 0 else 0
        self.__name = name if name is not None else "ko có tên"
        self.__price = price if price >=0 else 0
    @property
    def stock(self):
        return self.__stock
    @stock.setter
    def stock(self,so_luong_moi):
        if so_luong_moi <0:
            print("lỗi số")
        else:
            self.__stock = so_luong_moi
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,ten_moi):
        if ten_moi is None:
            print("ko dc để trống")
        else:
            self.__name = ten_moi
    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self,gia_moi):
        if gia_moi <=0:
            print("lỗi ko dc để giá")
        else:
            self.__price = gia_moi        
    def hien_thi_thong_tin(self):
        return f"Mặt hàng:{self.__name},Giá:{self.__price},Tồn kho:{self.__stock}"
    def nhap_hang(self,so_luong):
        if so_luong <= 0:
            return False
        self.__stock += so_luong
        print(f"đã nhập thêm {so_luong} vào {self.__name} tồn kho: {self.__stock}")
        return True
    def ban_hang(self,so_luong):
        if so_luong <= 0 or so_luong > self.__stock:
            return False
        self.__stock -= so_luong
        print(f"đã bán {self.__name} với số lượng {so_luong} tồn kho:{self.__stock}")
        return True 
    @abstractmethod
    def tinh_thue(self):
        pass