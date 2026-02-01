from fastapi import APIRouter, HTTPException
from app.services.fuzzy_detector import FuzzyDetector
from app.services.term_selector import TermSelector
from app.services.clause_segmenter import ClauseSegmenter
from app.services.classifier_service import VSMClassifier
import os
import fitz

router = APIRouter()
fuzzy_service = FuzzyDetector()
knapsack_service = TermSelector()
segmenter = ClauseSegmenter()
vsm_classifier = VSMClassifier()

@router.post("/{doc_id:path}/run")
async def run_full_analysis(doc_id: str):
    file_path = os.path.join("uploads_storage", doc_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        # 1. Text Extraction
        doc = fitz.open(file_path)
        document_text = "".join([page.get_text() for page in doc])
        doc.close()

        # 2. VSM Domain Classification
        domain_info = vsm_classifier.predict_domain(document_text)

        # 3. Dynamic Term Selection via Graph Centrality
        raw_terms = knapsack_service.extract_dynamic_terms(document_text)
        cloud_data = knapsack_service.optimize_word_cloud(raw_terms)

        # 4. Lawformer Risk Analysis
        clauses = segmenter.segment(document_text)
        risks = await fuzzy_service.identify_risks(clauses)

        return {
            "doc_id": doc_id,
            "domain_context": domain_info,
            "clauses": clauses,
            "risks": risks,
            "word_cloud": cloud_data,
            "status": "analysis_complete"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))