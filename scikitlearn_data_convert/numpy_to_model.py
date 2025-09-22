import numpy as np
from sklearn.linear_model import LogisticRegression

# (1) 입력 데이터 X: 2차원 배열 (샘플 4개, 특성 2개)
X = np.array([
    [25, 30000],   # 나이 25, 수입 3만
    [35, 50000],
    [45, 80000],
    [22, 20000]
])

# (2) 정답 y: 1차원 배열 (샘플 4개)
y = np.array([0, 1, 1, 0])  # 예: 0 = 구매 안함, 1 = 구매함

# (3) 모델 만들기
model = LogisticRegression()

# (4) 모델 학습
model.fit(X, y)

# (5) 새 데이터로 예측
X_new = np.array([[30, 40000]])  # 나이 30, 수입 4만
y_pred = model.predict(X_new)

print("예측 결과:", y_pred)
