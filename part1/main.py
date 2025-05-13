from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import json

# Selenium tự động tìm ChromeDriver

options = webdriver.ChromeOptions()

prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

# Mở trang web
driver.get("https://books.toscrape.com/")

time.sleep(3)

category = driver.find_element(By.XPATH, '//a[normalize-space()="Sequential Art"]')
print(f"Chọn danh mục {category.text}")

actions = ActionChains(driver)
actions.move_to_element(category).click().perform()




# Đường dẫn tới thư mục lưu file (cùng cấp với part1)
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "..", "data", "part1")
backup_dir = os.path.join(base_dir, "..", "data", "html_backup")

os.makedirs(save_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)
# Đường dẫn file json
save_path = os.path.join(save_dir, "books.json")

# Đọc dữ liệu cũ nếu có
if os.path.exists(save_path):
    with open(save_path, "r", encoding="utf-8") as f:
        all_books = json.load(f)
else:
    all_books = []


current_page = 0
while True:
    books = driver.find_elements(By.CSS_SELECTOR, "li.col-xs-6.col-sm-4.col-md-3.col-lg-3")
    print("Số lượng sách trong trang:", len(books))
    html = driver.page_source
    filename = f"html_page{current_page+1}.txt"
    save_html_path = os.path.join(backup_dir, filename)
    with open(save_html_path, "w", encoding="utf-8") as f:
         f.write(html)

    for book in books:
        book_href = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", book_href)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        
        title = driver.find_element(By.CSS_SELECTOR, "div.col-sm-6.product_main h1").text
        price = driver.find_element(By.CSS_SELECTOR, "div.col-sm-6.product_main p").text
        stock = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6.product_main p")[1].text
        star_rating = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6.product_main p")[2].get_attribute("class")
        rating_text = star_rating.split()[-1]
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating_number = rating_map.get(rating_text, 0)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        book_data = {
            "Title": title,
            "Price": price,
            "Availability": stock,
            "Product Page Link": book_href,
            "Star Rating": rating_number
        }
        all_books.append(book_data)
        # Lưu dữ liệu vào file JSON
        with open(save_path, "w", encoding="utf-8") as f:
                json.dump(all_books, f, ensure_ascii=False, indent=4)

    # Xử lý chuyển trang
    if len(driver.find_elements(By.CSS_SELECTOR, 'li.next')) > 0:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
        actions.move_to_element(next_button).click().perform()
        current_page += 1
        time.sleep(2)
    else:
        print("Không còn trang tiếp theo.")
        break

driver.quit()