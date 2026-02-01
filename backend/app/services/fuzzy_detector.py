from app.ml.lawformer_handler import lawformer
from sentence_transformers import util
import torch


class FuzzyDetector:
    def __init__(self):
        # Expanded seeds across Criminal, Contract, and Education law
        self.seed_terms = [
            "reasonable time", "material breach", "due diligence",
            "minor offence", "fair practice", "best efforts",
            "as per section", "probation period", "termination notice"
        ]

    async def identify_risks(self, clauses: list[str], threshold: float = 0.65):
        if not clauses: return []
        clause_embeddings = lawformer.get_embeddings(clauses)
        seed_embeddings = lawformer.get_embeddings(self.seed_terms)
        similarities = util.cos_sim(clause_embeddings, seed_embeddings)

        results = []
        for i, scores in enumerate(similarities):
            max_score = float(torch.max(scores))
            if max_score > threshold:
                results.append({
                    "clause_index": i,
                    "clarity_score": round(1 - max_score, 2),
                    "matched_concept": self.seed_terms[int(torch.argmax(scores))]
                })
        return results