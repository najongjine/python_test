# pip install pillow

from pathlib import Path
from PIL import Image

def convert_webp_to_png(root_folder):
    root = Path(root_folder)
    webp_files = list(root.rglob("*.webp"))

    print(f"총 {len(webp_files)}개의 .webp 파일을 찾았습니다.")

    for webp_path in webp_files:
        try:
            img = Image.open(webp_path).convert("RGBA")  # 알파 채널 포함
            png_path = webp_path.with_suffix(".png")
            img.save(png_path, "PNG")
            print(f"✅ 변환 완료: {webp_path.name} → {png_path.name}")
            
            # 변환이 성공하면 .webp 파일 삭제
            webp_path.unlink()
            print(f"🗑️ 삭제 완료: {webp_path.name}")

        except Exception as e:
            print(f"❌ 변환 실패: {webp_path} - {e}")


# 사용 예:
# convert_webp_to_png("/content/drive/MyDrive/dataset/images")
