from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import shutil
from app.services.ocr_service import OCRService

# Use APIRouter instance for modular routing
router = APIRouter()
UPLOAD_DIR = "uploads_storage"
ocr_service = OCRService()

@router.post("/upload") # Note: The prefix "/documents" is added in api_router.py
async def upload_document(file: UploadFile = File(...)):
    """
    Receives a file, saves it temporarily to disk, and triggers OCR.
    """
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger OCR service logic
        # extracted_text = ocr_service.extract_text_from_pdf(file_location)

        return {
            "filename": file.filename,
            "status": "success",
            "message": "File uploaded successfully to backend."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")