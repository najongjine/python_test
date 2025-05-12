"""
차 번호판 인식기

https://mj-thump-thump-story.tistory.com/entry/OCR-Tesseract-Windows-%ED%99%98%EA%B2%BD%EC%97%90-%EC%85%8B%EC%97%85
- tesseract 설치

https://jihoonch.tistory.com/4
-다른 사람이 만든 번호판 인식기
"""
import cv2
import numpy as np
import easyocr
from google.colab.patches import cv2_imshow

def detect_text(image_path):
    # EasyOCR 리더 초기화
    reader = easyocr.Reader(['ko', 'en'])

    # 이미지 읽기
    image = cv2.imread(image_path)
    if image is None:
        print(f"이미지를 불러올 수 없습니다: {image_path}")
        return

    # EasyOCR로 텍스트 감지
    result = reader.readtext(image)

    detected_plates = []

    # 결과 처리 및 시각화
    for (bbox, text, prob) in result:
        if len(text) >= 7 and any(char.isdigit() for char in text):  # 번호판 형식에 가까운 텍스트만 선택
            # 바운딩 박스 좌표
            (tl, tr, br, bl) = bbox
            tl = tuple(map(int, tl))
            br = tuple(map(int, br))

            # 텍스트 영역에 사각형 그리기
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)

            # 텍스트 출력
            cv2.putText(image, text, (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            detected_plates.append((text, prob))

    # 결과 이미지 표시
    cv2_imshow(image)

    return detected_plates

# 이미지 처리
image_paths = ['00.jpg', '01.jpg', '02.jpg', '03.jpg', '04.jpg',
               '05.jpg', '06.jpg', '07.jpg', '08.jpg', '09.jpg',
               '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg']

for path in image_paths:
    print(f"Processing {path}")
    plates = detect_text(path)
    if plates:
        for text, prob in plates:
            print(f"감지된 번호판: {text} (신뢰도: {prob:.2f})")
    else:
        print("감지된 번호판이 없습니다.")
    print()

