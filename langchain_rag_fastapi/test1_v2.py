from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import google.generativeai as genai
import uvicorn
import numpy as np
import faiss

# ✅ 설정
# faiss vector db가 있는 폴더. 소스코드랑 같은 경로에 있으면 그냥 비워두면 됨
save_path = ""
# 어느나라 언어든, 문장을 숫자로 바꿔주는 놈
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
    # ✅ 쿼리 벡터화 + 정규화
    query_vec = embedding_model.embed_query(query)
    query_vec = np.array([query_vec], dtype="float32")
    faiss.normalize_L2(query_vec)

    # ✅ FAISS 검색 (내적 기반 cosine 유사도)
    k = 10
    distances, indices = vector_db.index.search(query_vec, k)

    # ✅ 문서 및 점수 가져오기
    docs_and_scores = []
    for idx, score in zip(indices[0], distances[0]):
        if idx == -1:
            continue
        doc = vector_db.docstore.search(str(idx))
        docs_and_scores.append((doc, score))  # score는 cosine similarity (0~1)

    # ✅ 필터링
    threshold = 0.75
    filtered_docs = [doc for doc, score in docs_and_scores if score >= threshold]

    # ✅ 로그
    print(f"[총 검색된 문서 수]: {len(docs_and_scores)}")
    print(f"[필터링된 문서 수]: {len(filtered_docs)}")
    for i, (doc, score) in enumerate(docs_and_scores, 1):
        print(f"📄 문서 {i} | 유사도 점수: {score:.3f}")

    # ✅ 문서 연결
    context = "\n".join([doc.page_content for doc in filtered_docs])

    # ✅ 프롬프트 생성
    prompt = f"""
당신은 문서 기반 질문에 답하는 AI입니다.
다음 문서를 참고해서 질문에 답하십시오:

문서:
{context}

질문:
{query}

답변:
"""

    # ✅ Gemini API 호출
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

@app.post("/ask_manual_sample")
async def ask_question(request: QueryRequest):
    answer = """
    당신은 문서 기반 질문에 답하는 AI입니다.
다음 문서를 참고해서 질문에 답하십시오:
판매하는 상품 : 뱀, 호랑이, 쥐

    """
    return {
        "query": request.query,
        "answer": answer
    }

# ✅ 로컬 실행용 (uvicorn 으로 실행)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
