from fastapi import APIRouter
from app.services.network_service import NetworkService

router = APIRouter()
graph_service = NetworkService()


@router.get("/{doc_id}/dependency")
async def get_structure(doc_id: str):
    # Simulated clauses for Day 2 logic validation
    sample_clauses = [
        "Section 1: The parties agree to a lease term of 12 months.",
        "Section 2: Rental payments must be made as per Section 1.",
        "Section 3: Breach of Section 2 leads to immediate termination."
    ]

    graph_data = graph_service.build_dependency_graph(sample_clauses)
    return graph_data