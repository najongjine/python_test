"""
pip install rembg
pip install onnxruntime
"""

from rembg import remove
from PIL import Image
import io
import os

# 원본 이미지 불러오기
input_path = 'cat_n_person_20250618_162312_142_1.png'  # 제거할 대상 이미지
output_path = 'output.png'  # 배경 제거된 이미지 저장 경로

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, input_path)

with open(input_path, 'rb') as input_file:
    input_data = input_file.read()

# 배경 제거
output_data = remove(input_data)

# 저장
with open(output_path, 'wb') as output_file:
    output_file.write(output_data)

print("✅ 배경 제거 완료!")
