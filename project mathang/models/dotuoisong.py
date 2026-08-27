from models.mathang import MatHang
class TuoiSong(MatHang):
    def __init__(self, name, price, stock,han_dung:int):
        super().__init__(name, price, stock)
        self.__handung = han_dung
    @property
    def han_dung(self):
        return self.__handung
    @han_dung.setter
    def han_dung(self,han_dung_moi:int):
        if han_dung_moi < 0 :
            print("lỗi")
        else:
            self.__handung = han_dung_moi
            print("thay đổi hạn:", {self.__handung})
    def hien_thi_thong_tin(self):
        cha = super().hien_thi_thong_tin()
        return f"{cha}, hạn dùng: {self.__handung}"
    def tinh_thue(self):
        return self.price *0.02
