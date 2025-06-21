# 단일 파일

import torch
from PIL import Image
import cv2
import numpy as np
import os
from datetime import datetime

# 모델 불러오기 (YOLOv5s, 빠름)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 원하는 클래스 이름 (예: 'cat')
target_class = 'cat'

# 이미지 경로
image_filename = 'cat_n_cat.png'
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, image_filename)
img = Image.open(file_path)

# 감지 실행
results = model(img)

# 결과에서 필요한 정보만 추출
boxes = results.pandas().xyxy[0]  # 결과를 pandas로 추출
print(f"## 1st boxes:{boxes}")

# 원하는 클래스만 필터링
boxes = boxes[boxes['name'] == target_class]
print(f"## 2nd boxes:{boxes}")

# 출력 디렉토리
script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 .py 파일의 경로
output_dir = os.path.join(script_dir, "output")          # output 폴더 경로 결합
os.makedirs(output_dir, exist_ok=True)                   # 폴더 생성

for i, row in boxes.iterrows():
    xmin, ymin, xmax, ymax = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
    
    # 원본 이미지 열기 (OpenCV로)
    orig = cv2.imread(file_path)

    # 객체 부분 자르기
    cropped = orig[ymin:ymax, xmin:xmax]

    # 비율 유지하며 224x224 안에 맞추기
    h, w = cropped.shape[:2]
    scale = 224 / max(w, h)
    resized = cv2.resize(cropped, (int(w * scale), int(h * scale)))

    # 224x224 크기의 검은 배경 만들기
    canvas = np.zeros((224, 224, 3), dtype=np.uint8)
    
    # 중앙 정렬
    top = (224 - resized.shape[0]) // 2
    left = (224 - resized.shape[1]) // 2
    canvas[top:top+resized.shape[0], left:left+resized.shape[1]] = resized

    now = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
    print(type(image_filename))
    # 저장
    cv2.imwrite(f"output/{image_filename.split('.')[0][:100]}_{now}{i}.png", canvas)

print("완료!")
