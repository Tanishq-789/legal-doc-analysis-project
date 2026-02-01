import pytesseract
from pdf2image import convert_from_path
import os


class OCRService:
    def extract_text_from_pdf(self, pdf_path: str):
        """Processes scanned copies to editable content[cite: 628]."""
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        full_text = ""

        for i, image in enumerate(images):
            # Apply OCR to each image page
            page_text = pytesseract.image_to_string(image)
            full_text += f"\n--- Page {i + 1} ---\n" + page_text

        return self._normalize_text(full_text)

    def _normalize_text(self, text: str):
        """Standardizes text, retaining legal abbreviations[cite: 631]."""
        # Minimalist cleaning to preserve domain-specific meaning
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return " ".join(lines)