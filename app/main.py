from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth

app = FastAPI(
    title="MCP Brandwatch API",
    description="API untuk integrasi MCP dengan Brandwatch",
    version="1.0.0"
)

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["autentikasi"])

@app.get("/")
async def root():
    return {"message": "Selamat datang di MCP Brandwatch API"} 