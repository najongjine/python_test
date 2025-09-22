from sklearn.linear_model import LogisticRegression

# (1) 입력 X: list of lists (2차원)
X = [
    [25, 30000],
    [35, 50000],
    [45, 80000],
    [22, 20000]
]

# (2) 정답 y: list (1차원)
y = [0, 1, 1, 0]  # 0=구매 안함, 1=구매함

# (3) 모델 학습
model = LogisticRegression()
model.fit(X, y)

# (4) 새 데이터 예측
X_new = [[30, 40000]]
y_pred = model.predict(X_new)

print("예측 결과:", y_pred)
