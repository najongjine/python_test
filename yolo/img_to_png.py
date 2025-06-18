
"""
pip install pillow-avif-plugin

"""
import os
from PIL import Image
import mimetypes
import pillow_avif  # ✅ AVIF 지원

mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/avif', '.avif')
mimetypes.add_type('image/tiff', '.tiff')
mimetypes.add_type('image/tiff', '.tif')
mimetypes.add_type('image/svg+xml', '.svg')

# 입력과 출력 동일한 폴더
image_dir = "C:/Users/itg/Documents/python_test/yolo/convert_test"
os.makedirs(image_dir, exist_ok=True)

# 허용된 확장자
allowed_exts = ['.jpg', '.jpeg', '.png']

# 폴더 내 모든 파일 검사
for filename in os.listdir(image_dir):
    filepath = os.path.join(image_dir, filename)
    print(f"mimetypes.guess_type(filepath):{mimetypes.guess_type(filepath)}")

    # MIME 타입 확인
    mimetype_guess, _ = mimetypes.guess_type(filepath)
    if mimetype_guess is None or not mimetype_guess.startswith("image"):
        print("continue mimetype_guess")
        continue  # 이미지가 아니면 건너뜀

    ext = os.path.splitext(filename)[1].lower()
    if ext in allowed_exts:
        print("continue allowed_exts")
        continue  # 허용된 확장자면 변환 안 함

    try:
        with Image.open(filepath) as img:
            img = img.convert("RGBA")  # PNG는 투명도 지원
            base_name = os.path.splitext(filename)[0]
            print(base_name)
            output_path = os.path.join(image_dir, f"{base_name}.png")
            img.save(output_path, format='PNG')
            print(f"[✅] Converted {filename} → {base_name}.png")

        # 변환 성공 시 원본 삭제
        os.remove(filepath)
        print(f"[🗑️] Deleted original file: {filename}")

    except Exception as e:
        print(f"[⚠️] Failed to convert {filename}: {e}")
