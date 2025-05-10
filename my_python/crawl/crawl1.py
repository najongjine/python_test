"""
pip install requests
pip install beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup

# 1. 웹 페이지 요청
url = 'https://news.naver.com'
response = requests.get(url)

# 2. HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 3. 기사 제목 추출
titles = soup.select('.cluster_text_headline')

# 4. 결과 출력
for idx, title in enumerate(titles, 1):
    print(f"{idx}. {title.get_text().strip()}")