from fastapi import APIRouter
from app.api.endpoints import upload, analysis, classify, graph

api_router = APIRouter()

# These prefixes determine the final URL (e.g., /api/v1/documents/upload)
api_router.include_router(upload.router, prefix="/documents", tags=["ingestion"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["nlp-analysis"])
api_router.include_router(classify.router, prefix="/classification", tags=["classification"])
api_router.include_router(graph.router, prefix="/structural", tags=["graph-theory"])