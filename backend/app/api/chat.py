from fastapi import APIRouter, Request

from backend.app.models.chat import ChatRequest, ChatResponse

from backend.app.services.claude_service import generate_claude_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, chat_request: ChatRequest):
    claude_client = request.app.state.claude_client

    answer = await generate_claude_response(
            client=claude_client,
            question=chat_request.question
    )

    return ChatResponse(
        status="success",
        message=answer
    )
