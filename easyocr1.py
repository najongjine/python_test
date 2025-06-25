import easyocr
import matplotlib.pyplot as plt
from PIL import Image

# 1. OCR Reader 생성 (한글 + 영어)
reader = easyocr.Reader(['ko', 'en'])  # 한글/영어 인식

# 2. 이미지 경로
image_path = 'q3.png'  # 한글이 포함된 이미지

# 3. OCR 수행
results = reader.readtext(image_path)

# 4. 결과 출력
for bbox, text, confidence in results:
    print(f"인식된 텍스트: {text}, 정확도: {confidence:.2f}")
