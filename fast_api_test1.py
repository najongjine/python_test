from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Optional

from langchain.vectorstores import FAISS
import google.generativeai as genai

# ▶ FastAPI 인스턴스 생성
app = FastAPI()

# ▶ FAISS 로드
save_path = "/content/drive/MyDrive/dataset/embedding"
embedding_model = ...  # 여기에 당신이 쓰는 임베딩 모델 객체를 넣으세요 (예: HuggingFaceEmbeddings 등)
vector_db = FAISS.load_local(save_path, embedding_model, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 10})

# ▶ Gemini 설정
genai.configure(api_key="AIzaSyCj_KP3tWm9_3cgbjvQrZl5vv2M3_DBfZ0")
model = genai.GenerativeModel("gemini-2.5-flash")

# ▶ 함수 정의
def gemini_rag_answer(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""
당신은 문서 기반 질문에 답하는 AI입니다.
다음 문서를 참고해서 질문에 답하십시오:

문서:
{context}

질문:
{query}

답변:
"""
    response = model.generate_content(prompt)
    return response.text

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
