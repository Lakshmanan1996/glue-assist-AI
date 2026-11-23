from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from anthropic import AsyncAnthropic

from backend.app.core.secrets_manager import get_secret
from backend.app.api.health import router as health_router
from backend.app.api.chat import router as chat_router


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = get_secret("anthropic-api-key")
    app.state.claude_client = AsyncAnthropic(api_key=api_key)

    print("Claude Client initialized successfully")

    yield

    await app.state.claude_client.close()


app = FastAPI(
    title="Glue Assist AI",
    description="NOC Knowledge Assistant API",
    version="1.0.0",
    lifespan=lifespan
)


# Register API routes BEFORE frontend static files
app.include_router(health_router)
app.include_router(chat_router)


# Frontend homepage
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# Mount frontend LAST so it cannot intercept API requests
app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend"
)
