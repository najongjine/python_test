import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

engine = create_engine(DB_URL)

# 1) 바로 DataFrame으로
df = pd.read_sql(text("SELECT * FROM my_table"), engine)

# 2) X/y 분리
y = df["target"]
X = df.drop(columns=["target"])

num_cols = X.select_dtypes(include=["number"]).columns
cat_cols = X.select_dtypes(include=["object", "category"]).columns

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])

model = make_pipeline(preprocess, LogisticRegression(max_iter=1000))
model.fit(X, y)
