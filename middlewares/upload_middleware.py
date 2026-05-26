"""
middlewares/upload_middleware.py
Xử lý upload ảnh sản phẩm - tương đương Multer trong Node.js
Dùng Pillow để resize/nén ảnh (tương đương Sharp)
"""
import os
import uuid
from PIL import Image
from django.conf import settings


# ============================================================
# CẤU HÌNH UPLOAD
# ============================================================
DINH_DANG_CHO_PHEP = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
DUOI_FILE_CHO_PHEP = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
KICH_THUOC_TOI_DA = 5 * 1024 * 1024  # 5MB


def tao_thu_muc(duong_dan: str) -> None:
    """Tạo thư mục nếu chưa tồn tại"""
    os.makedirs(duong_dan, exist_ok=True)


def tao_ten_file_an_toan(file_goc) -> str:
    """
    Tạo tên file không trùng lặp, an toàn.
    KHÔNG dùng tên gốc từ người dùng (tránh Path Traversal, Unicode issues).
    """
    duoi = os.path.splitext(file_goc.name)[1].lower()
    if duoi not in DUOI_FILE_CHO_PHEP:
        duoi = '.jpg'
    return f"{uuid.uuid4().hex}{duoi}"


def kiem_tra_file(file) -> tuple[bool, str]:
    """
    Kiểm tra file upload:
    1. Định dạng (MIME type)
    2. Kích thước
    Trả về (True, '') nếu hợp lệ, (False, 'lý do') nếu không.
    """
    # Kiểm tra kích thước
    if file.size > KICH_THUOC_TOI_DA:
        return False, f"Kích thước file quá lớn. Tối đa {KICH_THUOC_TOI_DA // (1024*1024)}MB."

    # Kiểm tra MIME type
    content_type = file.content_type
    if content_type not in DINH_DANG_CHO_PHEP:
        return False, "Chỉ chấp nhận file ảnh (JPG, PNG, GIF, WEBP)."

    return True, ''


def xu_ly_va_luu_anh(file, thu_muc_con: str = 'san-pham') -> str:
    """
    Xử lý và lưu ảnh sản phẩm:
    1. Kiểm tra hợp lệ
    2. Resize về tối đa 800x800 (giữ tỷ lệ)
    3. Nén về JPEG chất lượng 85%
    4. Lưu vào MEDIA_ROOT/uploads/{thu_muc_con}/

    Trả về đường dẫn tương đối để lưu vào DB,
    hoặc raise ValueError nếu lỗi.
    """
    # Bước 1: Kiểm tra file
    hop_le, loi = kiem_tra_file(file)
    if not hop_le:
        raise ValueError(loi)

    # Bước 2: Tạo thư mục lưu
    thu_muc_luu = os.path.join(settings.MEDIA_ROOT, 'uploads', thu_muc_con)
    tao_thu_muc(thu_muc_luu)

    # Bước 3: Tạo tên file an toàn (luôn lưu thành .jpg sau khi nén)
    ten_file = f"{uuid.uuid4().hex}.jpg"
    duong_dan_day_du = os.path.join(thu_muc_luu, ten_file)

    # Bước 4: Mở ảnh và xử lý bằng Pillow (tương đương Sharp trong Node.js)
    try:
        with Image.open(file) as img:
            # Chuyển sang RGB để tránh lỗi khi lưu JPEG (PNG có thể có alpha)
            if img.mode in ('RGBA', 'P', 'LA'):
                # Tạo nền trắng cho ảnh có transparency
                nen_trang = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                nen_trang.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = nen_trang
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize về tối đa 800x800, giữ tỷ lệ, không phóng to ảnh nhỏ
            img.thumbnail((800, 800), Image.Resampling.LANCZOS)

            # Lưu với nén JPEG chất lượng 85%
            img.save(duong_dan_day_du, 'JPEG', quality=85, optimize=True)

    except Exception as e:
        raise ValueError(f"Không thể xử lý ảnh: {str(e)}")

    # Bước 5: Trả về đường dẫn tương đối (để lưu vào DB)
    duong_dan_tuong_doi = f"/media/uploads/{thu_muc_con}/{ten_file}"
    return duong_dan_tuong_doi


def xoa_anh_cu(duong_dan_cu: str) -> None:
    """
    Xóa ảnh cũ khi cập nhật ảnh mới.
    Chỉ xóa nếu file tồn tại và không phải ảnh mặc định.
    """
    if not duong_dan_cu or 'mac-dinh' in duong_dan_cu or 'default' in duong_dan_cu:
        return

    # Chuyển từ URL tương đối sang đường dẫn thực
    if duong_dan_cu.startswith('/media/'):
        ten_file = duong_dan_cu.replace('/media/', '', 1)
        duong_dan_thuc = os.path.join(settings.MEDIA_ROOT, ten_file)
    else:
        return

    if os.path.exists(duong_dan_thuc):
        try:
            os.remove(duong_dan_thuc)
        except OSError:
            pass  # Bỏ qua nếu không xóa được