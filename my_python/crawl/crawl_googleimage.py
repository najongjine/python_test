from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import urllib.request

# 크롬 웹드라이버 실행, 브라우저의 창을 최대화로 설정
options = ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# 구글 이미지로 이동
url = 'https://images.google.com/'  
driver.get(url)

searchKeyword="아름다운 자연"
# 원하는 이미지 검색
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.send_keys(searchKeyword + Keys.ENTER)  # 유재석 대신 입력하고 싶은 것을 입력

# 스크롤 다운
elem = driver.find_element(By.TAG_NAME, 'body')
for i in range(1):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# 더보기 처리
try:
    view_more_button = WebDriverWait(driver, 10).utill(EC.element_to_be_clickable((By.CLASS_NAME, 'mye4qd')))
    view_more_button.click()
    for i in range(10):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
except:
    pass

# 이미지 다운로드하기
# 신문사 로고의 경우 YQ4gaf zr758c라 이것도 수집되어, 사진만 추출할 수 있도록 코드 추가함
images = driver.find_elements(By.CSS_SELECTOR, ".YQ4gaf")
images = [img for img in images if img.get_attribute("class") == "YQ4gaf"]  

links = []
for image in images:
    src = image.get_attribute('src')
    if src is None:
        src = image.get_attribute('data-src')  # data-src도 확인
    if src:
        links.append(src)
        
print('찾은 이미지의 개수: ', len(links))

base_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(base_path, "imgs")
os.makedirs(save_path, exist_ok=True)  # 폴더가 없으면 생성

for k, i in enumerate(links):
    url = i
    file_path = os.path.join(save_path, f"{searchKeyword}{k}.png") 
    urllib.request.urlretrieve(url, file_path)

print('다운로드를 완료하였습니다.')