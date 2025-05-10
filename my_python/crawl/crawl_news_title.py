import requests
from bs4 import BeautifulSoup

# 네이버 뉴스 트렌드 페이지 URL
url = 'https://news.naver.com/main/ranking/popularDay.naver'

# HTTP 요청 헤더 설정 (User-Agent를 설정하여 봇으로 인식되지 않도록 함)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

# 페이지 요청
response = requests.get(url, headers=headers)

# 응답 상태 코드 확인
if response.status_code == 200:
    #파이썬은 if 문이나 for, while 같은 제어문 블록이 새로운 스코프(scope)를 생성하지 않습니다. 함수나 클래스: 새로운 지역 스코프를 생성합니다.
    html = response.text
    print("HTML 가져오기 성공")
else:
    print(f"페이지 요청 실패: {response.status_code}")
    exit

# HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 뉴스 기사 리스트 선택
articles = soup.select('div.rankingnews_box a')

# 뉴스 제목과 링크 출력
for idx, article in enumerate(articles, 1):
    title = article.get_text(strip=True)
    link = article['href']
    print(f"{idx}. {title}")
    print(f"   링크: {link}")
