from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from app.config import settings
from app.auth import verify_bearer_token
from app.rate_limiter import rate_limiter
from app.cost_guard import budget_tracker
from utils.mock_llm import MockLLM


def load_system_prompt() -> str:
    try:
        with open(settings.SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Bạn là TravelBuddy, trợ lý du lịch thân thiện."


SYSTEM_PROMPT = load_system_prompt()
llm = MockLLM()


def run_agent(user_message: str) -> str:
    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ])
    return response["answer"]


app = FastAPI(title=settings.APP_NAME)


class ChatRequest(BaseModel):
    user_id: str = "student"
    message: str
    estimated_cost_usd: float = 0.1


class ChatResponse(BaseModel):
    user_id: str
    answer: str
    estimated_cost_usd: float
    spent_this_month_usd: float
    budget_remaining_usd: float


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "message": "TravelBuddy API is running with Mock LLM."
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    _: str = Depends(verify_bearer_token)
):
    if not rate_limiter.allow(payload.user_id, settings.RATE_LIMIT_PER_MINUTE):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    if not payload.message.strip():
        raise HTTPException(status_code=422, detail="Message must not be empty.")

    if not budget_tracker.check_budget(payload.user_id, payload.estimated_cost_usd):
        raise HTTPException(status_code=402, detail="Monthly budget exceeded.")

    answer = run_agent(payload.message)

    budget_tracker.add_cost(payload.user_id, payload.estimated_cost_usd)
    spent = budget_tracker.get_spent(payload.user_id)
    remaining = max(0.0, settings.MONTHLY_BUDGET_USD - spent)

    return ChatResponse(
        user_id=payload.user_id,
        answer=answer,
        estimated_cost_usd=payload.estimated_cost_usd,
        spent_this_month_usd=spent,
        budget_remaining_usd=remaining
    )