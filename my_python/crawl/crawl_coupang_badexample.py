"""
쿠팡에서 개 사료를 검색한다음 top 10 제품을 크롤링 하려고 한다.
하지만 이 코드를 실행하면 파이썬이 얼어버린것처럼 결과가 안나온다.
쿠팡 크롤링 시 발생하는 문제
동적 콘텐츠 로딩: 쿠팡은 JavaScript를 통해 페이지 콘텐츠를 동적으로 로딩합니다. 따라서 requests로 가져온 HTML에는 원하는 상품 정보가 포함되지 않을 수 있습니다.

봇 탐지 및 차단: 쿠팡은 비정상적인 접근을 탐지하여 차단하는 시스템을 운영합니다. 이는 User-Agent, IP 주소, 요청 빈도 등을 분석하여 결정됩니다.
"""

import requests
from bs4 import BeautifulSoup

# 쿠팡 검색 URL
search_query = '개 사료'
url = f'https://www.coupang.com/np/search?q={search_query}&sort=scoreDesc'

# HTTP 요청 헤더 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

# 페이지 요청
response = requests.get(url, headers=headers)

# 응답 상태 코드 확인
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # 상품 리스트 선택
    products = soup.select('ul.search-product-list li.search-product')
    # 상위 10개 상품 추출
    for idx, product in enumerate(products[:10], 1):
        title_tag = product.select_one('div.name')
        link_tag = product.select_one('a.search-product-link')
        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            link = 'https://www.coupang.com' + link_tag['href']
            print(f"{idx}. {title}")
            print(f"   링크: {link}")
else:
    print(f"페이지 요청 실패: {response.status_code}")
