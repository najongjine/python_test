import requests

API_TOKEN = ""  # 발급받은 토큰으로 교체
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

def answer_question(question, context):
    payload = {"inputs": {"question": question, "context": context}}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result["answer"]

context = "Hugging Face is a company based in New York City. Its mission is to democratize artificial intelligence."
question = "Where is Hugging Face based?"

print(answer_question(question, context))
