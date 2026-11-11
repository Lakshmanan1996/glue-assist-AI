from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=3, max_length=2000)


class ChatResponse(BaseModel):
    status: str
    message: str
