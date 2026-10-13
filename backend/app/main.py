from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .config import settings
from .faq import retrieve
from .gemini import generate_answer

FALLBACK = "I don't have verified information about that. Please contact the college office."
app = FastAPI(title="College FAQ Chatbot")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_methods=["POST", "GET"], allow_headers=["Content-Type"])

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

class Source(BaseModel):
    id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    question = body.message.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Message cannot be blank")
    matches = retrieve(question)
    if not matches:
        return ChatResponse(answer=FALLBACK, sources=[])
    try:
        answer = await generate_answer(question, matches)
    except Exception:
        raise HTTPException(status_code=503, detail="Answer service temporarily unavailable")
    if not answer or "I don't have verified information" in answer:
        return ChatResponse(answer=FALLBACK, sources=[])
    return ChatResponse(answer=answer, sources=[Source(id=f["id"], question=f["question"]) for f in matches])
