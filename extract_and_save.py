# lấy dữ liệu lazada: lưu SQL

# Thư viện selenium dùng để điều khiển trình duyệt chrome tự động 
from selenium import webdriver
from selenium.webdriver.common.by import By # dùng để chọn phần tử html
from selenium.webdriver.chrome.service import Service # dùng để quản lý trình điều khiển chrome
from webdriver_manager.chrome import ChromeDriverManager # tự động tải trình điều khiển chrome
import time # dùng để tạm dừng chương trình

#import ham ket noi MySQL tu file db.py
from db import get_connection

#===============================
#Ham 1: Lay du lieu tu lazada bang selenium 
#===============================

def get_lazada_data(keyword="dien thoai"):
    # tao cau hinh trinh duyet chrome
    # headless=new de chrome chay an, khong hien cua so
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    # khoi tao trinh duyet chrome
    #chromeDriverManager tu dong tai dung phien ban chromedriver phu hop
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
# mo url tim kiem lazada theo tu khoa
    url = f"https://www.lazada.vn/catalog/?q={keyword}"
    driver.get(url)

    # cho 3s de web load hoan toan
    time.sleep(3)

    # cuon xuong page de lazy-load du lieu
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(1)

    # tim tat ca cac san pham tren trang
    # mot so selector thong dung cua Lazada
    product_selectors = [".Bm3ON", ".c2prKC", "div[data-qa-locator='product-item']", "div[data-sqe='item']"]
    products = []
    for sel in product_selectors:
        products = driver.find_elements(By.CSS_SELECTOR, sel)
        if products:
            print(f"Tim duoc {len(products)} san pham voi selector '{sel}'")
            break

    if not products:
        print("Khong tim duoc san pham, kiem tra selector cua trang Lazada")

    # Danh sach de chua du lieu lay duoc
    data = []

    # Lay 10 san pham dau tien
    for p in products[:10]:
        try:
            # lay ten san pham (mot so selectors thong dung)
            title = ""
            for s in [".RfADt", ".CVE4o", ".c16H9d", "a[title]", "h1"]:
                try:
                    title = p.find_element(By.CSS_SELECTOR, s).text
                    if title:
                        break
                except Exception:
                    continue

            # lay gia san pham
            price = ""
            for s in [".ooOxS", ".p5dt7f", ".c3gUWw", ".c13VH6"]:
                try:
                    price = p.find_element(By.CSS_SELECTOR, s).text
                    if price:
                        break
                except Exception:
                    continue

            # lay so luong da ban (khong phai san pham nao cung co)
            try:
                sold = p.find_element(By.CSS_SELECTOR, ".gAeZC").text
            except Exception:
                sold = "khong ro"

            # lay danh gia san pham
            try:
                rating = p.find_element(By.CSS_SELECTOR, ".Lh7ru").text
            except Exception:
                rating = "chua co"

            # Lay hinh anh san pham tu the <img>
            img = p.find_element(By.TAG_NAME, "img").get_attribute("src")

            # lay link san pham tu the <a>
            link = p.find_element(By.TAG_NAME, "a").get_attribute("href")

            # them 1 tuple du lieu vao danh sach data
            data.append((title, price, sold, rating, img, link))
        except Exception:
            # neu san pham bi loi hoac thieu du lieu -> bo qua
            continue

            # dong trinh duyet de giai phong tai nguyen 
    driver.quit()

    # tra ve danh sach du lieu lay duoc
    return data

#===============================
#Ham 2: Luu du lieu vao MySQL
#===============================

def save_to_mysql(data):
    # mo ket noi MySQL qua ham get_connection()
    conn = get_connection()
    cursor = conn.cursor()

    # Tao bang neu chua ton tai
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lazada_products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            price VARCHAR(100),
            sold VARCHAR(100),
            rating VARCHAR(100),
            img TEXT,
            link TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # Cau SQL INSERT du lieu vao bang lazada_products
    sql = """
        INSERT INTO lazada_products (title, price, sold, rating, img, link)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    if data:
        cursor.executemany(sql, data)
        conn.commit()
        print(f"Da luu {cursor.rowcount} ban ghi vao MySQL thanh cong!")
    else:
        print("Khong co du lieu de luu.")

    conn.close()


#===============================
# Phan main chay chuong trinh
#===============================
if __name__ == "__main__":
    # 1. Goi ham lay du lieu tu lazada bang selenium
    data = get_lazada_data()

    # 2. Goi ham de luu du lieu vao MySQL
    save_to_mysql(data)

    # ket qua
    # - selenium mo lazada -> lay 10 san pham dau tien -> tra ve list data
    #- MySQL luu data vao bang lazada_products

    

