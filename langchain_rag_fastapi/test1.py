from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import google.generativeai as genai
import uvicorn

# ✅ 설정
# faiss vector db가 있는 폴더. 소스코드랑 같은 경로에 있으면 그냥 비워두면 됨
save_path = ""
# 어느나라 언어든, 문장을 숫자로 바꿔주는 놈
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")  # 예시
"""
👉 FAISS 벡터 데이터베이스를 저장된 파일에서 불러오는 코드입니다.

왜 embedding_model이 필요하죠?
👉 검색할 문장을 벡터로 바꾸기 위해서입니다.
저장된 FAISS 인덱스는 예를 들어 384차원짜리 벡터로 만들었는데,
검색할 문장도 같은 방식으로 384차원으로 만들어야 비교할 수 있어요.
"""
vector_db = FAISS.load_local(save_path, embedding_model, allow_dangerous_deserialization=True)

"""
👉 벡터 DB를 **"검색기(retriever)"**로 바꿔주는 함수입니다.
"""
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
    """
    사용자의 질문을 벡터로 변환해 벡터 DB에서 유사한 문서를 검색하고,
    유사도가 높은 문서만 골라 Gemini에게 전달해 답변을 생성하는 함수입니다.
    """
    # 유사도 점수까지 같이 가져오기 (k=10)
    docs_and_scores = vector_db.similarity_search_with_score(query, k=10)
    for i, (doc, score) in enumerate(docs_and_scores, 1):
        print(f"📄 문서 {i}")
        print(f"🔹 유사도 점수: {score}")
        print(f"🔹 문서 내용 요약: {doc.page_content[:100]}...\n")

    # ✅ 유사도 기준 필터링 (cosine 유사도 기준: 높을수록 좋음, 예: 0.75 이상만 사용)
    threshold = 0.7
    filtered_docs = [doc for doc, score in docs_and_scores if score >= threshold]

    # 로그 출력 (필터링 전/후 확인용)
    print(f"[총 검색된 문서 수]: {len(docs_and_scores)}")
    print(f"[필터링된 문서 수]: {len(filtered_docs)}")

    # 문서 내용을 하나로 연결
    context = "\n".join([doc.page_content for doc in filtered_docs])

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
