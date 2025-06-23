from ultralytics import YOLO
import cv2
import numpy as np
import os

# ✅ 모델 로드
model = YOLO('yolov8m_face.pt')  # 얼굴 탐지 전용 모델 사용 (사전 준비되어 있어야 함)

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

# ✅ 하나의 이미지에서 얼굴 crop
def crop_faces_from_image(image_path, output_dir, image_name_prefix="face"):
    img = cv2.imread(image_path)
    results = model(img)
    boxes = results[0].boxes.xyxy.cpu().numpy()

    for idx, (x1, y1, x2, y2) in enumerate(boxes):
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        face = img[y1:y2, x1:x2]
        face_resized = resize_with_padding(face, (224, 224))

        out_path = os.path.join(output_dir, f"{image_name_prefix}_{idx+1}.jpg")
        cv2.imwrite(out_path, face_resized)
        print(f"✅ 저장됨: {out_path}")

# ✅ 입력 폴더 전체 처리
def crop_faces_from_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_folder, filename)
            name_prefix = os.path.splitext(filename)[0]  # ex: google_0050
            crop_faces_from_image(input_path, output_folder, name_prefix)

# ✅ 실행: 입력 폴더와 출력 폴더 경로 지정
input_folder_path = "C:/Users/itg/Documents/python_test/AutoCrawler/download/Pak_Myung_Su"     # 👉 입력 폴더명 (이미지들이 있는 곳)
output_folder_path = "C:/Users/itg/Documents/python_test/AutoCrawler/download/Pak_Myung_Su_cropped"   # 👉 출력 폴더명

crop_faces_from_folder(input_folder_path, output_folder_path)
