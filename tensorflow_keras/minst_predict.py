"""
1. 손글씨 이미지를 준비한다 (내가 그린 숫자)
2. 이미지 크기/채널을 MNIST처럼 전처리한다 (28×28, 흑백)
3. 모델을 불러온다 (.h5 파일)
4. 모델에 이미지를 넣어서 예측한다
5. 예측 결과를 숫자로 해석한다
"""

# 이미지 불러오기 & 흑백으로 변환
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# 손글씨 이미지 경로
image_path = 'my_digit.png'

# 1. 이미지 로드 (흑백)
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 2. 크기 조정 (MNIST는 28x28)
img = cv2.resize(img, (28, 28))

# 3. 흰 배경이면 반전 (MNIST는 검은 배경에 흰 글씨)
if np.mean(img) > 127:
    img = 255 - img

# 4. 정규화 및 shape 변형
img = img.astype('float32') / 255.0
img = img.reshape(1, 28, 28, 1)  # 배치 차원 추가


model = load_model('my_mnist_99.34acc_2.42loss.h5')


pred = model.predict(img)  # 확률 벡터
predicted_label = np.argmax(pred)  # 가장 높은 확률의 인덱스가 정답

print(f"모델이 예측한 숫자: {predicted_label}")


plt.imshow(img.reshape(28, 28), cmap='gray')
plt.title(f"Predicted: {predicted_label}")
plt.axis('off')
plt.show()
