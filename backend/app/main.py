from fastapi import FastAPI

from backend.app.core.secrets_manager import get_secret

from contextlib import asynccontextmanager

from backend.app.api.health import router as health_router

from backend.app.api.chat import router as chat_router

from anthropic import AsyncAnthropic

#Add Secret Manager startup integration

@asynccontextmanager
async def lifespan(app:FastAPI):
    api_key = get_secret("anthropic-api-key")
    app.state.claude_client = AsyncAnthropic(
            api_key=api_key
    )
    print("Claude Client initialized successfully")
    
    yield

    await app.state.claude_client.close()



# Create FastAPI application
app = FastAPI(
    title="Glue Assist AI",
    description="NOC Knowledge Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# First API endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Glue Assisti AI"
    }

app.include_router(health_router)
app.include_router(chat_router)
