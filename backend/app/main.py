from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.upload import router as upload_router
from app.api.routes.analyze import router as analyze_router
from app.api.routes.projects import router as projects_router

app = FastAPI(
    title="RIVA Backend API",
    version="2.0.0"
)

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Support /upload, /api/upload, /api/analyze, and /api/projects
app.include_router(upload_router)
app.include_router(upload_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(projects_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to RIVA"
    }