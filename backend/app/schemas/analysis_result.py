from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DomainContext(BaseModel):
    predicted_domain: str
    confidence: float
    algorithm_used: str

class RiskDetail(BaseModel):
    clause_index: int
    matched_anchor: str
    clarity_score: float
    risk_level: str

class WordCloudItem(BaseModel):
    text: str
    weight: int
    value: int

class FullAnalysisResponse(BaseModel):
    doc_id: str
    domain_context: DomainContext
    visualization_evidence: List[str] = Field(..., description="The 'Responsible Words' for highlighting")
    clauses: List[str]
    risks: List[RiskDetail]
    word_cloud: List[WordCloudItem]
    status: str