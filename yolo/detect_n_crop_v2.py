import torch
from PIL import Image
import cv2
import numpy as np
import os
from datetime import datetime

# 모델 불러오기
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 감지할 대상 클래스
target_class = 'cat'

# 예: 입력 images 폴더. 안의 모든 이미지 처리
input_dir = "C:/Users/itg/Documents/python_test/yolo/source"   

# 출력 이미지 폴더 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output")
os.makedirs(output_dir, exist_ok=True)

# 처리할 이미지 확장자들
valid_exts = ['.jpg', '.jpeg', '.png']

# 폴더 내 모든 이미지 반복
for image_filename in os.listdir(input_dir):
    if not any(image_filename.lower().endswith(ext) for ext in valid_exts):
        continue  # 이미지 파일이 아니면 skip

    print(f"\n[🔍] Processing: {image_filename}")
    file_path = os.path.join(input_dir, image_filename)
    
    try:
        img = Image.open(file_path)
    except Exception as e:
        print(f"[⚠️] 이미지 열기 실패: {e}")
        continue

    results = model(img)
    boxes = results.pandas().xyxy[0]
    boxes = boxes[boxes['name'] == target_class]

    if boxes.empty:
        print(f"[ℹ️] No '{target_class}' detected in {image_filename}")
        continue

    for i, row in boxes.iterrows():
        xmin, ymin, xmax, ymax = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
        orig = cv2.imread(file_path)

        if orig is None:
            print(f"[⚠️] OpenCV로 이미지 로딩 실패: {file_path}")
            continue

        cropped = orig[ymin:ymax, xmin:xmax]
        h, w = cropped.shape[:2]
        scale = 224 / max(w, h)
        resized = cv2.resize(cropped, (int(w * scale), int(h * scale)))

        canvas = np.zeros((224, 224, 3), dtype=np.uint8)
        top = (224 - resized.shape[0]) // 2
        left = (224 - resized.shape[1]) // 2
        canvas[top:top+resized.shape[0], left:left+resized.shape[1]] = resized

        now = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        safe_name = image_filename.split('.')[0][:100]  # 확장자 제거 + 최대 100자
        save_path = os.path.join(output_dir, f"{safe_name}_{now}_{i}.png")
        cv2.imwrite(save_path, canvas)

    print(f"[✅] {len(boxes)} object(s) saved from {image_filename}")

print("\n🎉 모든 이미지 처리 완료!")
