from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, os, requests
from urllib.parse import quote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

script_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(script_dir, "chromedriver.exe")

def fetch_image_urls(query, max_links_to_fetch):
    
    search_url = f"https://www.google.com/search?q={quote(query)}&tbm=isch&tbs=isz:l"

    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
    #options.add_argument("--headless")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(search_url)

    image_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while len(image_urls) < max_links_to_fetch:
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
        print(f"Found {len(thumbnails)} thumbnails")

        for img in thumbnails[len(image_urls):max_links_to_fetch]:
            try:
                img.click()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
                )
                images = driver.find_elements(By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')
                for image in images:
                    src = image.get_attribute('src')
                    if src and src.startswith('http') and "encrypted-tbn0" not in src:
                        image_urls.add(src)
                        print(f"Collected: {src}")
                        if len(image_urls) >= max_links_to_fetch:
                            break
            except Exception as e:
                print(f"Skip due to error: {e}")
                continue

        # 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return list(image_urls)

def download_images(keyword, limit=10, save_dir='download'):
    os.makedirs(f"{save_dir}/{keyword}", exist_ok=True)
    urls = fetch_image_urls(keyword, limit)
    for i, url in enumerate(urls):
        try:
            img_data = requests.get(url, timeout=5).content
            with open(f"{save_dir}/{keyword}/{keyword}_{i:03}.jpg", 'wb') as f:
                f.write(img_data)
            print(f"Saved: {keyword}_{i:03}.jpg")
        except Exception as e:
            print(f"Failed to download {url} - {e}")

if __name__ == "__main__":
    keyword = input("검색어를 입력하세요: ")
    download_images(keyword, limit=1)
