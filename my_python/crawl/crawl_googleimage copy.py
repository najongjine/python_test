from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, urllib.request

# 검색어 설정
search_query = "아름다운 자연"

# 저장 폴더
save_dir = "beautiful_nature_images"
os.makedirs(save_dir, exist_ok=True)

# ChromeDriver 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(script_dir, 'chromedriver.exe')
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# 구글 이미지 검색 페이지 열기
driver.get("https://www.google.co.kr/imghp?hl=ko")

# 검색어 입력 및 엔터
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# 이미지 썸네일 기다리기 (명시적 대기)
try:
    thumbnails = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.Q4LuWd"))
    )
except:
    print("이미지 썸네일을 찾을 수 없습니다.")
    driver.quit()
    exit()

print(f"썸네일 개수: {len(thumbnails)}")

# 이미지 3개 다운로드
for i in range(3):
    try:
        thumbnails[i].click()
        time.sleep(2)
        images = driver.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
        for image in images:
            src = image.get_attribute("src")
            if src and src.startswith("http"):
                urllib.request.urlretrieve(src, os.path.join(save_dir, f"image_{i+1}.jpg"))
                print(f"{i+1}번 이미지 저장 완료!")
                break
    except Exception as e:
        print(f"{i+1}번 이미지 실패: {e}")

driver.quit()
