import requests

API_TOKEN = "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"  # 발급받은 토큰으로 교체
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_text(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result[0]["generated_text"]

print(generate_text("Once upon a time"))
