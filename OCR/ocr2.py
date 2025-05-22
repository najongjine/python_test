import cv2
import pytesseract
import os

# Tesseract 설치 경로 지정
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# 이미지 경로 (업로드한 파일명과 일치하도록 수정)
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'c2.jpg')

# 이미지 읽기
image = cv2.imread(image_path)
if image is None:
    print("이미지를 불러올 수 없습니다.")
    exit()
else:
    print("이미지를 성공적으로 불러왔습니다.")

# 이미지 전처리: 회색조, 대비 향상, 이진화
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)  # 노이즈 제거
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# 화면에 보여주기 (번호판이 작을 경우 확대)
scale = 2.0
resized = cv2.resize(thresh, None, fx=scale, fy=scale)

# OCR 설정: --psm 7은 단일 라인, --oem 3은 LSTM OCR 엔진 사용
config = '--oem 3 --psm 7 -l kor'

# 텍스트 인식
text = pytesseract.image_to_string(resized, config=config)

# 결과 출력
print("인식된 번호판 텍스트:", text.strip())

# 이미지 보기 (디버깅용)
cv2.imshow('전처리된 이미지', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
