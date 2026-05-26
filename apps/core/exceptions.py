class LoiTuyChon(Exception):
    """Lớp cơ sở cho các lỗi tùy chỉnh trong hệ thống"""
    def __init__(self, thong_bao, ma_http, ma_loi, chi_tiet=None):
        super().__init__(thong_bao)
        self.thong_bao = thong_bao
        self.ma_http = ma_http
        self.ma_loi = ma_loi
        self.chi_tiet = chi_tiet

class LoiKhongTimThay(LoiTuyChon):
    def __init__(self, tai_nguyen):
        super().__init__(f"Không tìm thấy {tai_nguyen}", 404, 'NOT_FOUND')

class LoiDuLieuKhongHopLe(LoiTuyChon):
    def __init__(self, chi_tiet=None):
        super().__init__("Dữ liệu không hợp lệ", 400, 'VALIDATION_ERROR', chi_tiet)

class LoiKhongCoQuyen(LoiTuyChon):
    def __init__(self):
        super().__init__("Bạn không có quyền thực hiện hành động này", 403, 'FORBIDDEN')