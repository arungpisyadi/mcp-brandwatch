from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, brandwatch

app = FastAPI(
    title="MCP Brandwatch API",
    description="API for MCP integration with Brandwatch",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["authentication"])
app.include_router(brandwatch.router, prefix="/api/brandwatch", tags=["brandwatch"])

@app.get("/")
async def root():
    return {"message": "Welcome to MCP Brandwatch API"} 