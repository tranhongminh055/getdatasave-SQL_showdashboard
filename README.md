# Tích hợp dữ liệu Lazada (Selenium + MySQL + Flask)

Dự án thực hiện ETL: lấy sản phẩm từ Lazada, lưu vào MySQL, và hiển thị bằng Flask.

## 1. Yêu cầu
- Python 3.8+
- MySQL server (hoặc MariaDB)
- Trình duyệt Chrome

## 2. Cài đặt
1. Mở terminal ở folder dự án:
```powershell
cd "g:\TÍCH HỢP DỮ LIỆU QUA MÔ HÌNH PRESENTATION"
```
2. Cài thư viện Python:
```powershell
pip install selenium webdriver-manager flask pymysql cryptography
```

## 3. MySQL
1. Tạo database `shop`:
```sql
CREATE DATABASE shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
2. Cập nhật thông tin kết nối trong `db.py` nếu cần:
- host
- user
- password
- database

## 4. Chạy thu thập dữ liệu
```powershell
python extract_and_save.py
```
- Script sẽ gọi Selenium, tìm `40` sản phẩm đầu trang Lazada, lưu `10` sản phẩm vào bảng `lazada_products`.
- Thông báo trên console: `Tim duoc ...`, `Da luu ...`.

## 5. Chạy web Flask
```powershell
python app.py
```
- Mở: `http://localhost:5000`
- Giao diện sẽ hiển thị sản phẩm từ bảng `lazada_products`.

## 6. Mở rộng
- Thay `products[:10]` thành `products[:40]` trong `extract_and_save.py` để lưu nhiều hơn.
- Chỉnh selector nếu Lazada đổi cấu trúc HTML.
- Thêm API JSON, endpoint `/api/products` nếu cần.
