import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# CSV 파일 불러오기
df = pd.read_csv("spam_email.csv", encoding="utf-8")

# 데이터 확인 (처음 5개만 보기)
print(df.head())

# 입력값 (링크 여부, 스팸 단어 포함 여부 등)
X = df[["링크포함", "스팸단어포함", "짧은메일", "느낌표개수"]]

# 정답값 (이메일이 스팸인지 아닌지)
y = df["스팸여부"]

# 70%는 훈련용, 30%는 테스트용으로 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# 모델 만들기
model = LogisticRegression()

# 학습시키기
model.fit(X_train, y_train)

# 테스트 데이터로 예측해보기
accuracy = model.score(X_test, y_test)
print("정확도:", accuracy)

# 예: 새 이메일 특징 입력 (링크O, 스팸단어O, 짧음, 느낌표 2개)
new_email = [[1, 0, 0, 0]]

prediction = model.predict(new_email)
print("스팸 여부 예측 결과:", "스팸" if prediction[0] == 1 else "정상")