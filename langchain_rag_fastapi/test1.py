from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import google.generativeai as genai
import uvicorn

# ✅ 설정
save_path = ""
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")  # 예시
vector_db = FAISS.load_local(save_path, embedding_model, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 8})

# ✅ Gemini API 설정
genai.configure(api_key="AIzaSyCj_KP3tWm9_3cgbjvQrZl5vv2M3_DBfZ0")
model = genai.GenerativeModel("gemini-2.5-flash")

# ✅ FastAPI 앱 정의
app = FastAPI()

# ✅ 요청 형식 정의
class QueryRequest(BaseModel):
    query: str

# ✅ 응답 처리 함수
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

# ✅ 엔드포인트 정의
@app.post("/ask")
async def ask_question(request: QueryRequest):
    answer = gemini_rag_answer(request.query)
    return {
        "query": request.query,
        "answer": answer
    }

# ✅ 로컬 실행용 (uvicorn 으로 실행)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
