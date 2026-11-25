from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    customer_id: str = Field(min_length=1, max_length=100)

    document_type: Optional[
        Literal["ticket_process", "patch_process"]
    ] = None


class ChatResponse(BaseModel):
    status: str
    message: str
