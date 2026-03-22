from fastapi import APIRouter, HTTPException
from app.services.fuzzy_detector import FuzzyDetector
from app.services.term_selector import TermSelector
from app.services.clause_segmenter import ClauseSegmenter
from app.services.classifier_service import VSMClassifier
from app.services.domain_router import DomainRouter
import os
import fitz
import logging

# Initialize logging for the Uvicorn error stream
logger = logging.getLogger("uvicorn.error")

router = APIRouter()

# Global service instances
vsm_classifier = VSMClassifier()
segmenter = ClauseSegmenter()
knapsack_service = TermSelector()
domain_router = DomainRouter()


@router.post("/{doc_id:path}/run")
async def run_full_analysis(doc_id: str):
    """
    Executes the Orchestrated Legal NLP Pipeline with Edge Case Handling:
    1. Text Extraction Guard: Identifies empty/scanned documents.
    2. Domain Pivot: Handles 'General Legal' fallbacks for out-of-domain docs.
    3. Multi-Algorithmic Evidence: Merges Lawformer attention with VSM/FSM anchors.
    """

    # 1. Initialize variables to ensure scope safety
    document_text = ""
    predicted_domain = "General Legal"
    lawformer_evidence = []
    dispatch_result = {"algorithm": "Keyword-Density-Analyzer", "responsible_words": [], "identified_risks": []}
    clauses = []
    cloud_data = []

    file_path = os.path.abspath(os.path.join("uploads_storage", doc_id))
    logger.info(f"--- [START] Orchestrated Analysis: {doc_id} ---")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {doc_id} not found.")

    try:
        # STEP 1: Text Extraction & Scanned PDF Guard
        logger.info(f"--- [1/5] Extracting text ---")
        with fitz.open(file_path) as doc:
            for page in doc:
                document_text += page.get_text().strip() + " "

        # --- EDGE CASE 1: NO SEARCHABLE TEXT ---
        # If the PDF is a scan or an image, get_text() returns an empty string.
        if not document_text.strip():
            logger.warning(f"--- [GUARD] No text detected in {doc_id} (Possible Scan) ---")
            return {
                "doc_id": doc_id,
                "status": "error",
                "error_type": "EMPTY_DOCUMENT",
                "detail": "No searchable text found. Please upload a PDF with a text layer (OCR)."
            }

        # STEP 2: Domain Classification (Lawformer + Heuristics)
        logger.info(f"--- [2/5] Predicting Domain ---")
        domain_info = vsm_classifier.predict_domain(document_text)

        predicted_domain = domain_info.get("predicted_domain", "General Legal")
        lawformer_evidence = domain_info.get("raw_evidence", [])
        confidence = domain_info.get("confidence", 0.0)

        logger.info(f"Result: {predicted_domain} ({confidence})")

        # STEP 3: Domain-Specific Dispatching (The "Pivot")
        # --- EDGE CASE 2: OUT-OF-DOMAIN HANDLING ---
        # If 'General Legal' is passed, the router will use the default analyzer.
        logger.info(f"--- [3/5] Dispatching to specialized algorithm for: {predicted_domain} ---")
        dispatch_result = await domain_router.route_and_analyze(
            domain=predicted_domain,
            text=document_text
        )

        # STEP 4: Adaptive Segmentation
        logger.info(f"--- [4/5] Segmenting clauses ---")
        clauses = segmenter.segment(document_text)

        # STEP 5: Evidence Merging & Knapsack Optimization
        logger.info(f"--- [5/5] Finalizing visualization data ---")

        # Combine attention-based words (ML) with structural anchors (Algorithmic)
        total_evidence = list(set(lawformer_evidence + dispatch_result.get("responsible_words", [])))

        # Extract graph-based candidates and optimize the cloud display
        candidate_terms = knapsack_service.extract_dynamic_terms(document_text)
        cloud_data = knapsack_service.optimize_word_cloud(
            term_data=candidate_terms,
            priority_terms=total_evidence
        )

        logger.info(f"--- [SUCCESS] Analysis pipeline complete for {doc_id} ---")

        return {
            "doc_id": doc_id,
            "domain_context": {
                "predicted_domain": predicted_domain,
                "confidence": confidence,
                "algorithm_used": dispatch_result.get("algorithm"),
                "is_fallback": predicted_domain == "General Legal"
            },
            "visualization_evidence": total_evidence,
            "clauses": clauses,
            "risks": dispatch_result.get("identified_risks", []),
            "word_cloud": cloud_data,
            "status": "analysis_complete"
        }

    except Exception as e:
        logger.error(f"--- [CRITICAL ERROR] Pipeline Failed: {str(e)} ---")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis Engine Error: {str(e)}"
        )