"""
차 번호판 인식기

https://mj-thump-thump-story.tistory.com/entry/OCR-Tesseract-Windows-%ED%99%98%EA%B2%BD%EC%97%90-%EC%85%8B%EC%97%85
- tesseract 설치

https://jihoonch.tistory.com/4
-다른 사람이 만든 번호판 인식기
"""
import cv2
import pytesseract
import os
#C:\Program Files\Tesseract-OCR
# Tesseract 경로 설정 (Windows 사용자만 필요)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # 설치 경로에 따라 수정

# 스크립트의 디렉토리 경로
script_dir = os.path.dirname(os.path.abspath(__file__))

# 이미지 파일 경로
image_path = os.path.join(script_dir, 'c4.jpg')

# 이미지 읽기
image = cv2.imread(image_path)
if image is None:
    print("이미지를 불러올 수 없습니다.")
    exit()
else:
    print("이미지를 성공적으로 불러왔습니다.")

# 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 노이즈 제거를 위한 블러 처리
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 엣지 검출
edged = cv2.Canny(blurred, 100, 200)

# 윤곽선 찾기
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 가장 큰 윤곽선부터 확인
for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
    approx = cv2.approxPolyDP(cnt, 10, True)
    if len(approx) == 4:  # 사각형인지 확인
        x, y, w, h = cv2.boundingRect(cnt)
        plate = gray[y:y+h, x:x+w]
        break

# OCR로 텍스트 인식
text = pytesseract.image_to_string(plate, lang='kor')  # 한국어 인식을 위해 'kor' 사용
print("인식된 번호판:", text.strip())
