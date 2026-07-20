from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.logging import setup_logging
from core.exceptions import BaseAppException, app_exception_handler
from api.middleware.correlation import CorrelationIdMiddleware
from api.routers import ai_router

setup_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)

# Allow CORS for the Office Add-in frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to Add-in host domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(CorrelationIdMiddleware)
app.add_exception_handler(BaseAppException, app_exception_handler)

app.include_router(ai_router.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
