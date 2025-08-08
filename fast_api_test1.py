"""
pip install fastapi
pip install "uvicorn[standard]"
pip install langchain
pip install faiss-cpu
pip install sentence-transformers  # 또는 HuggingFaceEmbeddings 쓸 경우
pip install google-generativeai
pip install -U langchain-community
pip install fastapi "uvicorn[standard]" langchain faiss-cpu sentence-transformers google-generativeai

"""
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Optional
import os
import uvicorn

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import google.generativeai as genai

# ▶ FastAPI 인스턴스 생성
app = FastAPI()

# ▶ FAISS 로드
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 기준 디렉토리
save_path = os.path.join(current_dir, "embedding/rag")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vector_db = FAISS.load_local(save_path, embedding_model, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 8})

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

# ▶ GET API 엔드포인트
@app.get("/ask")
def ask(query: str = Query(..., description="질문을 입력하세요")):
    try:
        answer = gemini_rag_answer(query)
        return JSONResponse(content={"query": query, "answer": answer})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# ▶ 실행
if __name__ == "__main__":
    # host="0.0.0.0" : 모든 IP에서 접속 허용
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)