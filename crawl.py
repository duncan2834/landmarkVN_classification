from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# Danh sách danh lam thắng cảnh ở Việt Nam
landmarks = [
    "Vịnh Hạ Long", "Núi Yên Tử", "Hồ Hoàn Kiếm", "Văn Miếu - Quốc Tử Giám", "Chùa Một Cột",
    "Lăng Chủ tịch Hồ Chí Minh", "Phố cổ Hà Nội", "Thác Bản Giốc", "Hồ Ba Bể",
    "Hang Pác Bó", "Chùa Bái Đính", "Tràng An", "Tam Cốc - Bích Động", "Cố đô Hoa Lư",
    "Fansipan", "Ruộng bậc thang Sa Pa", "Chợ Bắc Hà", "Đèo Ô Quy Hồ", "Động Phong Nha",
    "Quảng trường Lâm Viên", "Động Thiên Đường", "Cố đô Huế",
    "Lăng Tự Đức", "Sông Hương", "Chùa Thiên Mụ", "Bà Nà Hills",
    "Ngũ Hành Sơn", "Phố cổ Hội An", "Chùa Cầu", "Thánh địa Mỹ Sơn",
    "Vịnh Lăng Cô", "Địa đạo Củ Chi", "Nhà thờ Đức Bà Sài Gòn",
    "Dinh Độc Lập", "Chợ Bến Thành", "Bưu điện Trung tâm Sài Gòn",
    "Chợ nổi Cái Răng", "Rừng tràm Trà Sư", "Núi Cấm", "Đảo Phú Quốc", "Bãi Sao",
    "Đỉnh Bàn Cờ", "Nhà thờ lớn Hà Nội", "Công viên Thiên văn học", "Lũng Cú", "Sơn Đoòng", "Hàm Cá Mập", "Nhà Thờ Đá"
]
print(len(landmarks))
# Thiết lập Selenium
chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Tạo thư mục để lưu ảnh
base_dir = "landmark_images"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
    
def download_image(url, folder, filename):
    try:
        response = requests.get(url, stream=True, timeout=10) # Gửi yêu cầu HTTP GET đến URL ảnh.
        if response.status_code == 200: # Kiểm tra xem máy chủ có trả về trạng thái thành công (200 OK) hay không., không thì là 404
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f: # mở file trong chế độ ghi nhị phân (wb) để lưu dữ liệu ảnh.
                f.write(response.content)
            print(f"Đã tải: {filename}")
        else:
            print(f"Lỗi tải ảnh: {url}")
    except Exception as e:
        print(f"Không thể tải ảnh {url}: {e}")
        
def crawl_images(landmark, num_images):
    # Tạo thư mục cho từng danh lam thắng cảnh
    folder = os.path.join(base_dir, landmark.replace(" ", "_"))
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Truy cập Google Images
    search_url = f"https://www.google.com/search?q={landmark}+Việt+Nam&tbm=isch" # tbm=isch là tham số giúp chuyển Google Search sang chế độ tìm ảnh.
    driver.get(search_url) # Truy cập trang web bằng Selenium

    # Lấy các phần tử ảnh
    image_urls = set() # để là set cho đỡ trùng
    skips = 0
    # Cuộn trang để tải thêm ảnh
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # Chờ ảnh tải 
    
    while len(image_urls) + skips < num_images:     
        thumbnails = driver.find_elements(By.CLASS_NAME, "YQ4gaf")
        for img in thumbnails[len(image_urls) + skips:num_images]:
            try:
                img.click()
                time.sleep(2)
            except:
                continue
            
            images = driver.find_elements(By.CLASS_NAME, "sFlh5c.FyHeAf.iPVvYb")    
            for image in images:
                if image.get_attribute('src') in image_urls:
                    num_images += 1
                    skips += 1
                    break
                
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
                    
    for i, url in enumerate(image_urls):
        filename = f"{landmark.replace(' ', '_')}_{i+1}.jpg"
        print(url)
        download_image(url, folder, filename)
            
# Crawl ảnh cho từng danh lam thắng cảnh
for landmark in landmarks:
    print(f"Đang crawl ảnh cho: {landmark}")
    crawl_images(landmark, num_images=20)
    time.sleep(3)  # Nghỉ giữa các lần tìm kiếm để tránh bị chặn

# Đóng trình duyệt
driver.quit()
print("Hoàn tất crawl ảnh!")