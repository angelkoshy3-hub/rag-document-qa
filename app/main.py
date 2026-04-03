from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.api import routes
from app.core.config import settings

# Initialize the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready FastAPI structure for a RAG system.",
    version="1.0.0",
)

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include the API routes with the configured prefix
app.include_router(routes.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["ui"])
async def read_root(request: Request):
    """
    Serve the web UI.
    """
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

# Global health check (can also be accessed at /api/v1/health)
@app.get("/health", tags=["status"])
async def root_health():
    """
    Root level health check.
    """
    return {"status": "ok", "message": f"Welcome to {settings.APP_NAME}"}

if __name__ == "__main__":
    import uvicorn
    # This allows running the app directly via: python app/main.py
    # But the recommended way is: uvicorn app.main:app --reload
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
