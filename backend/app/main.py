from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.api_router import api_router

app = FastAPI(
    title="Intelligent Legal Document Analysis API",
    version="1.0.0"
)

# Middleware
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root level check
@app.get("/")
def read_root():
    return {"message": "Legal Analysis API is Running"}

# Include the modular API routes
app.include_router(api_router, prefix="/api/v1")