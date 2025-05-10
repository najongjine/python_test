import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# 데이터셋 로드
# fashion_mnist: Zalando에서 제공하는 의류 이미지 데이터셋으로, 10가지 의류 종류로 분류됩니다.
fashion_mnist = keras.datasets.fashion_mnist
# load_data(): 데이터셋을 다운로드하고 훈련용과 테스트용으로 분리하여 로드합니다.​
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# 클래스 이름 정의. 각 클래스 레이블에 해당하는 의류 이름을 리스트로 정의합니다.
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# fashion_mnist 시각화
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[test_labels[i]])
plt.tight_layout()
plt.show()

# 데이터 정규화. 이미지 픽셀 값은 0255 범위의 정수입니다. 이를 01 범위로 정규화하여 모델 학습을 용이하게 합니다.​
train_images = train_images / 255.0
test_images = test_images / 255.0

# 모델 구성. Sequential: 층을 순차적으로 쌓는 모델입니다.
# Flatten: 2차원 입력(28x28)을 1차원 배열(784,)로 변환합니다.
# Dense(128, activation='relu'): 128개의 뉴런을 가진 완전 연결층으로, ReLU 활성화 함수를 사용합니다.
# Dense(10): 10개의 뉴런을 가진 출력층으로, 각 클래스에 대한 로짓 값을 출력합니다.
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),  # 28x28 이미지를 1D 배열로 변환
    keras.layers.Dense(128, activation='relu'),  # 은닉층
    keras.layers.Dense(10)  # 출력층 (10개 클래스)
])

# 모델 컴파일 및 학습
# optimizer='adam': Adam 최적화 알고리즘을 사용하여 모델을 학습시킵니다.
# loss=SparseCategoricalCrossentropy(from_logits=True): 다중 클래스 분류를 위한 손실 함수로, 로짓 값을 입력으로 받습니다.
# metrics=['accuracy']: 모델의 정확도를 평가 지표로 사용합니다.
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# 모델 학습. 모델을 10번 반복하여 훈련 데이터에 대해 학습시킵니다.
model.fit(train_images, train_labels, epochs=10)

# 모델 평가.
# evaluate: 테스트 데이터를 사용하여 모델의 손실과 정확도를 평가합니다.
# verbose=2: 평가 과정을 자세히 출력합니다.
# test_acc: 테스트 데이터에 대한 모델의 정확도를 출력합니다.
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print('\n테스트 정확도:', test_acc)

# 예측 및 시각화. 모델의 출력 로짓 값을 확률로 변환하기 위해 Softmax 층을 추가합니다.
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

# 테스트 이미지에 대한 예측 확률을 계산합니다.
predictions = probability_model.predict(test_images)

# 첫 번째 테스트 이미지를 시각화하고, 예측 결과와 실제 레이블을 제목으로 표시합니다.
plt.figure()
plt.imshow(test_images[0])
plt.colorbar()
plt.grid(False)
plt.title(f"predict: {class_names[np.argmax(predictions[0])]}, actual: {class_names[test_labels[0]]}")
plt.show()
