import pandas as pd
from sklearn.linear_model import LogisticRegression

# (1) DataFrame으로 입력값 X 만들기
X = pd.DataFrame({
    "age": [25, 35, 45, 22],       # 나이
    "income": [30000, 50000, 80000, 20000]  # 수입
})

# (2) Series로 정답 y 만들기
y = pd.Series([0, 1, 1, 0])  # 예: 0 = 구매 안함, 1 = 구매함

# (3) 모델 만들기
model = LogisticRegression()

# (4) 모델 학습
model.fit(X, y)

# (5) 새 데이터도 DataFrame으로 예측
X_new = pd.DataFrame({"age": [30], "income": [40000]})
y_pred = model.predict(X_new)

print("예측 결과:", y_pred)

