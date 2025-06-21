"""
pip install ultralytics opencv-python
pip install yolov8face

"""
from ultralytics import YOLO
import cv2
import numpy as np
import os

# ✅ 모델 로드 (공식 YOLOv8n 모델로 충분히 테스트됨)
model = YOLO('yolov8m_face.pt')  # 일반 객체 탐지 모델 (얼굴 class도 포함)

# ✅ 클래스 ID 0 = person, 얼굴 전용 모델 없을 경우 이걸 활용
# 원래 얼굴 전용 모델 yolov8n-face.pt 쓸 수 있으면 더 정확함

# ✅ 비율 유지 + 패딩
def resize_with_padding(image, size=(224, 224), pad_color=(0, 0, 0)):
    h, w = image.shape[:2]
    target_w, target_h = size

    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h))

    delta_w = target_w - new_w
    delta_h = target_h - new_h
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    padded = cv2.copyMakeBorder(resized, top, bottom, left, right,
                                 cv2.BORDER_CONSTANT, value=pad_color)
    return padded

# ✅ 얼굴 인식 + crop + 저장
def crop_faces_yolo(image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    img = cv2.imread(image_path)
    results = model(img)

    # box 좌표 가져오기
    boxes = results[0].boxes.xyxy.cpu().numpy()

    for idx, (x1, y1, x2, y2) in enumerate(boxes):
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        face = img[y1:y2, x1:x2]
        face_resized = resize_with_padding(face, (224, 224))

        out_path = os.path.join(output_dir, f"face_{idx+1}.jpg")
        cv2.imwrite(out_path, face_resized)
        print(f"✅ 저장됨: {out_path}")

# ✅ 실행
crop_faces_yolo("google_0050.jpg", "faces_output")
