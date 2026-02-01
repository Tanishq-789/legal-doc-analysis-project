# backend/app/main.py
import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
UPLOAD_DIR = "uploads_storage"

# Ensure upload directory exists upon startup
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Legal Doc Analysis API")

# --- Middleware ---
# Configure CORS to allow requests from your React frontend (Vite default port 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Analysis Backend API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Receives a file, saves it temporarily to disk, and returns a success status.
    """
    try:
        # Create a secure path for the file
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        # Write the incoming file bytes to disk
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"Successfully saved file to: {file_location}")

        # Return dummy data for now - Day 1 Goal achieved
        return {
            "filename": file.filename,
            "status": "success",
            "message": "File uploaded successfully to backend."
        }

    except Exception as e:
        print(f"Error during upload: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")