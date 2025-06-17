from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, requests
from urllib.parse import quote

script_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(script_dir, "chromedriver.exe")

def fetch_image_urls(keyword, max_links=5):
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)

    search_url = f"https://www.google.com/search?q={quote(keyword)}&tbm=isch"
    driver.get(search_url)
    time.sleep(2)

    image_urls = set()
    scroll_pause = 1

    while len(image_urls) < max_links:
        thumbs = driver.find_elements(By.CSS_SELECTOR, "div.isv-r.PNCib.MSM1fd.BUooTd")
        print(f"Found {len(thumbs)} thumbnails")

        for thumb in thumbs[len(image_urls):]:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", thumb)
                thumb.click()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
                )
                big_img = driver.find_element(By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb")
                src = big_img.get_attribute("src")
                if src and src.startswith("http"):
                    image_urls.add(src)
                    print("Collected:", src)
                    if len(image_urls) >= max_links:
                        break
            except Exception as e:
                print("Error:", e)
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

    driver.quit()
    return list(image_urls)

def download_images(keyword, limit=5):
    save_dir = os.path.join("download", keyword)
    os.makedirs(save_dir, exist_ok=True)
    urls = fetch_image_urls(keyword, limit)
    for i, url in enumerate(urls):
        try:
            response = requests.get(url, timeout=10)
            ext = url.split(".")[-1].split("?")[0]
            ext = ext if ext.lower() in ["jpg", "jpeg", "png"] else "jpg"
            filename = os.path.join(save_dir, f"{keyword}_{i:03}.{ext}")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Saved {filename}")
        except Exception as e:
            print("Download failed:", e)

if __name__ == "__main__":
    keyword = input("검색어를 입력하세요: ")
    download_images(keyword, limit=1)
