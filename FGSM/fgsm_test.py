import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# 🔧 설정
IMG_PATH = 'google_0001_1.jpg'  # 너가 올린 박명수 이미지
MODEL_PATH = 'your_model.h5'    # 훈련된 모델 경로 (업로드 필요)
IMG_SIZE = (224, 224)
EPSILON = 0.02  # 노이즈 강도

# 1. 모델 불러오기
model = load_model(MODEL_PATH)

# 2. 이미지 로드 및 전처리
img = image.load_img(IMG_PATH, target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = img_array / 255.0  # 정규화
input_img = np.expand_dims(img_array, axis=0)

# 3. FGSM 함수 정의 (non-targeted)
@tf.function
def create_adversarial_pattern(input_image, true_label):
    with tf.GradientTape() as tape:
        tape.watch(input_image)
        prediction = model(input_image)
        loss = tf.keras.losses.categorical_crossentropy(true_label, prediction)
    gradient = tape.gradient(loss, input_image)
    signed_grad = tf.sign(gradient)
    return signed_grad

# 4. 원래 클래스 예측
pred_orig = model.predict(input_img)
pred_label = np.argmax(pred_orig)
print("✅ 원래 예측:", pred_label)

# 5. one-hot 라벨 만들기
true_label = tf.one_hot(pred_label, depth=3)
true_label = tf.reshape(true_label, (1, 3))

# 6. 적대적 노이즈 생성
perturbations = create_adversarial_pattern(tf.convert_to_tensor(input_img), true_label)
adversarial_img = input_img + EPSILON * perturbations
adversarial_img = tf.clip_by_value(adversarial_img, 0, 1)

# 7. 적대 이미지 예측
pred_adv = model.predict(adversarial_img)
adv_label = np.argmax(pred_adv)
print("❌ 적대 이미지 예측:", adv_label)

# 8. 시각화
def show_images(orig, adv):
    fig, ax = plt.subplots(1, 2, figsize=(10,5))
    ax[0].imshow(orig[0])
    ax[0].set_title("원본 이미지")
    ax[1].imshow(adv[0])
    ax[1].set_title("적대적 이미지")
    plt.show()

show_images(input_img.numpy(), adversarial_img.numpy())
