#문장 분류, 감정 분석 등

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

inputs = tokenizer("I love teaching AI!", return_tensors="pt")
outputs = model(**inputs)
print(outputs.logits)
# 각 배열은 별점을 나타냄. [별점1,별점2,별점3...]
