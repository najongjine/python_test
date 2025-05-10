"""
크로니움 드라이버를 이용해서 크롤링 하던방식. 2024년 까지는 작동했으나 쿠팡에서 사이트 보안을 추가한후 막힘
"""

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_coupang(keyword):
    driver = setup_driver()
    driver.get("https://www.coupang.com/")

    try:
        # 팝업 닫기 (존재하는 경우)
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close"))
            )
            close_button.click()
        except:
            pass

        # 검색어 입력
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # 검색 결과 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-product"))
        )

        # 스크롤 다운 (더 많은 결과 로딩)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        products = driver.find_elements(By.CLASS_NAME, "search-product")

        results = []
        for product in products[:10]:  # 상위 10개 제품만 처리
            try:
                item = {}
                item['name'] = product.find_element(By.CLASS_NAME, "name").text
                item['price'] = product.find_element(By.CLASS_NAME, "price-value").text

                ahref = product.find_element(By.TAG_NAME, 'a')
                item['link'] = ahref.get_attribute('href')

                results.append(item)

            except:
                continue

        return results
    except TimeoutException:
        print("페이지 로딩 시간이 초과되었습니다. 네트워크 연결을 확인하거나 나중에 다시 시도해주세요.")
        return []
    except Exception as e:
        print(f"크롤링 중 오류가 발생했습니다: {str(e)}")
        return []
    finally:
        driver.quit()


def main():
    keyword = input("검색할 키워드를 입력하세요: ")
    results = search_coupang(keyword)

    if results:
        print(f"\n'{keyword}' 검색 결과:")
        for idx, result in enumerate(results, 1):
            print(f"{idx}. 제품명: {result['name']}")
            print(f"   가격: {result['price']}")
            print(f"   링크: {result['link']}")
            print("-" * 50)

        print(f"\n총 {len(results)}개의 제품이 검색되었습니다.")
    else:
        print("검색 결과를 가져오는 데 실패했습니다.")

if __name__ == "__main__":
    main()