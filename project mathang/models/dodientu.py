from models.mathang import MatHang
class DienTu(MatHang):
    def __init__(self, name, price, stock,baohanh:int):
        super().__init__(name, price, stock)
        self.__baohanh =  baohanh
    @property
    def baohanh(self):
        return self.__baohanh
    @baohanh.setter
    def baohanh(self,het_han_moi):
        if het_han_moi <0:
            print("lỗi")
        else:
            self.__baohanh = het_han_moi
            print(f"thời hạn còn lại:{self.__baohanh}")
    def hien_thi_thong_tin(self):
        thong_tin_cha = super().hien_thi_thong_tin()
        return f"{thong_tin_cha}, còn thời hạn:{self.__baohanh}"
    def tinh_thue(self):
        return self.price *0.1