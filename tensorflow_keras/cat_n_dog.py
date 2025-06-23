from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


# 데이터셋 다운로드
!wget https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip

# 압축 풀기
!unzip -q cats_and_dogs_filtered.zip


# 데이터 폴더
base_dir = 'cats_and_dogs_filtered'

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# 데이터 폴더/train data/cats
# 데이터 폴더/train data/dogs
train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')
print(f"train_cats_dir:{train_cats_dir}")
print(f"train_dogs_dir:{train_dogs_dir}")

# 데이터 폴더/test data/cats
# 데이터 폴더/test data/dogs
validation_cats_dir = os.path.join(validation_dir, 'cats')
validation_dogs_dir = os.path.join(validation_dir, 'dogs')

# 데이터 폴더/train data/cats에 있는 파일
# 데이터 폴더/train data/dogs에 있는 파일
train_cat_fnames = os.listdir(train_cats_dir)
train_dog_fnames = os.listdir(train_dogs_dir)

print(f"train_cat_fnames[:10]:{train_cat_fnames[:10]}")
print(f"train_dog_fnames[:10]:{train_dog_fnames[:10]}")

# training total number cats and dogs images in train and validation set
num_cats_train = len(os.listdir(train_cats_dir))
num_dogs_train = len(os.listdir(train_dogs_dir))

print("number of cats in train dir     : ", num_cats_train)
print("number of dogs in train dir     : ", num_dogs_train)

num_cats_validation = len(os.listdir(validation_cats_dir))
num_dogs_validation = len(os.listdir(validation_dogs_dir))

print('total validation cat images :', num_cats_validation)
print('total validation dog images :', num_dogs_validation)

total_train = num_cats_train + num_dogs_train
total_validation = num_cats_validation + num_dogs_validation

print("Total training images:", total_train)
print("Total validation images:", total_validation)



BATCH_SIZE = 100 # 한 번에 100장의 사진(데이터)을 가져와서 학습시킨다는 뜻이야.
EPOCHS = 100 # 전체 데이터를 몇 번 반복 학습할 건지 정하는 값이야.
IMG_HEIGHT = 150 #  사진 크기를 150x150 픽셀로 고정
IMG_WIDTH = 150

# seed 값 설정
seed = 15 # 랜덤 결과 고정 (언제 돌려도 동일하게)
np.random.seed(seed)
tf.random.set_seed(seed)


#train_generator → "학습용 데이터" 준비. 그냥 **"어떻게 변형할지 레시피(설정)만 저장"**한 상태. 이미지는 아직 손도 안 댐!
train_datagen = ImageDataGenerator(
    rescale=1./255, # 정규화(normalization)
    rotation_range=40, # 최대 40도까지 랜덤으로 회전
    width_shift_range=0.2, # 가로 방향으로 최대 20% 랜덤 이동
    height_shift_range=0.2, # 세로 방향으로 최대 20% 랜덤 이동
    shear_range=0.2, # 비스듬하게 찌그러뜨리기
    zoom_range=0.2, # 최대 20%까지 랜덤하게 확대/축소
    horizontal_flip=True, # 좌우반전
    fill_mode='nearest' # 회전하거나 이동해서 빈 공간이 생기면 → 그 공간을 "가장 가까운 색으로 채우기".
)


train_generator = train_datagen.flow_from_directory( # 그냥 "데이터 흐름 준비(generator 세팅)"만 한 상태.  "필요할 때 그때그때 이미지를 읽어서 numpy로 변환해주는 기계"를 만든 것
    directory=train_dir, # cats_and_dogs_filtered/train
    classes=['cats', 'dogs'], # 'cats' → 고양이 → label 0, 'dogs' → 강아지 → label 1   이렇게 라벨을 자동으로 붙여줌
    batch_size=BATCH_SIZE, # 한 번에 몇 장씩 읽어올지 정함
    shuffle=True, # 랜덤으로 섞어서
    target_size=(IMG_HEIGHT, IMG_WIDTH), # 이미지를 150x150으로 resize 해서 가져옴
    class_mode='binary' # 라벨이 0 또는 1로
)

# validation (검증) 용 데이터를 준비
validation_datagen = ImageDataGenerator(rescale=1./255) # 픽셀 값만 0~1로 정규화.   검증 데이터는 "진짜 평가"니까 → 원본 그대로 평가하는 게 좋음

validation_generator = validation_datagen.flow_from_directory(
    directory=validation_dir,
    classes=['cats', 'dogs'],
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)


# Model Creation.   [ Conv2D → MaxPooling → Conv2D → MaxPooling → Conv2D → MaxPooling → Flatten → Dense → Dense → Dense(출력) ]
model = tf.keras.models.Sequential([ # 층(layer)를 "위에서 아래로 순서대로" 쌓는 구조.   신경망(Neural Network) 모델을 만드는 부분
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(150, 150, 3)), # 이미지 특징(feature)를 뽑아냄. 필터 16개, 필터 크기 (3x3짜리 창으로 이미지 훑기), ReLU → 비선형성 추가, 입력 크기 (150x150, 컬러 → R/G/B → 3채널)
    tf.keras.layers.MaxPooling2D(2, 2), # 2x2 영역에서 가장 큰 값(max) 만 남김. 이미지 크기 절반으로 줄어듦 → 계산량 ↓ → 중요 특징만 남김.   보통 3~4번 정도까지만 하는 게 일반적

    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'), # 더 복잡한 특징 학습 (예: 고양이 눈, 개 귀 같은 패턴들!)
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'), # 더 고차원적인 특징 학습 (예: 고양이 전체 얼굴, 개 전체 몸통 패턴 등)
    tf.keras.layers.MaxPooling2D(2, 2), # 18 * 18 크기가 됨

    tf.keras.layers.Flatten(), # 지금까지 나온 2D 이미지 특징맵을 1D 벡터로 펴기
    tf.keras.layers.Dense(512, activation='relu'), # 완전 연결 층(Dense layer).    뉴런 512개 → 복잡한 조합 학습
    tf.keras.layers.Dense(64, activation='relu'), # 또 한 번 Dense layer.   더 깊은 패턴 학습
    tf.keras.layers.Dense(1, activation='sigmoid') # 출력층.   sigmoid → 출력값이 0~1 사이로 나옴
])


# compiling the model
model.compile(
    loss='binary_crossentropy',
    optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
    metrics=['accuracy']
)


# 모델 학습
history = model.fit( # numpy로 바뀌는 순간
    train_generator, # 학습용 데이터 (generator 형태)
    steps_per_epoch=int(np.ceil(total_train / float(BATCH_SIZE))), # epoch 당 몇 번 batch를 학습할지 정하는 값. 2000 / 100 = 20 steps.   → 한 epoch(1번 전체 학습)에서 → 20번 batch 학습함
    epochs=EPOCHS, # 총 몇 epoch 동안 학습할지 → 앞에서 EPOCHS = 100이면 100번 반복 학습
    validation_data=validation_generator, # 검증용 데이터 generator. 학습 중간중간 시험(validation)을 봄 → 성능 확인용
    validation_steps=int(np.ceil(total_validation / float(BATCH_SIZE))) # 검증할 때 몇 step(batch)를 돌릴지 정함. 1000 / 100 = 10 steps.   검증할 때 10번 batch를 평가함
)

# 정확도와 손실함수 시각화
acc =history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs_range=range(EPOCHS)
plt.figure(figsize=(8,8))
plt.subplot(2,1,1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(2,1,2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()