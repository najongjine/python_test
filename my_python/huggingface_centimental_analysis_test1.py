import requests

API_TOKEN = "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"  # 발급받은 토큰으로 교체
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

def analyze_sentiment(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result[0]

print(analyze_sentiment("I love this movie!"))
