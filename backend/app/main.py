# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Legal Doc Analysis API")

# Configure CORS to allow requests from your React frontend
# In production, replace "*" with your specific frontend domain
origins = [
    "http://localhost:5173", # Default Vite port
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Analysis Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}