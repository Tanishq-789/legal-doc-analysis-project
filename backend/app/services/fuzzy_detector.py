from app.ml.lawformer_handler import get_lawformer
from sentence_transformers import util
import torch
import logging

logger = logging.getLogger("uvicorn.error")


class FuzzyDetector:
    def __init__(self):
        self.lawformer = get_lawformer()

        # Categorized seeds for domain-specific "Responsible Word" extraction
        self.seeds = {
            "GENERAL": [
                "reasonable time", "material breach", "due diligence",
                "fair practice", "best efforts", "forthwith"
            ],
            "Education Law": [
                "FERPA", "Title IX", "Accreditation", "Pedagogy",
                "Tuition Waiver", "Academic Probation", "Syllabus Compliance",
                "Enrollment", "Faculty Tenure", "Student Privacy"
            ]
        }

        logger.info("--- [INIT] Pre-calculating Domain-Specific Fuzzy Seeds ---")
        self.seed_embeddings = {}
        with torch.no_grad():
            for domain, terms in self.seeds.items():
                self.seed_embeddings[domain] = self.lawformer.get_embeddings(terms)
        logger.info("--- [SUCCESS] Fuzzy Detector Ready ---")

    async def identify_risks(self, clauses: list[str], domain: str = "GENERAL", threshold: float = 0.70):
        """
        Pivots analysis based on domain. Returns responsible words for visualization
        instead of treating the whole clause as an opaque block.
        """
        if not clauses: return []

        # Choose the correct embedding set based on the Lawformer prediction
        active_seeds = self.seeds.get(domain, self.seeds["GENERAL"])
        active_embeddings = self.seed_embeddings.get(domain, self.seed_embeddings["GENERAL"])

        clause_embeddings = self.lawformer.get_embeddings(clauses)
        similarities = util.cos_sim(clause_embeddings, active_embeddings)

        results = []
        responsible_words = set()

        for i, scores in enumerate(similarities):
            max_score = float(torch.max(scores))
            if max_score > threshold:
                matched_idx = int(torch.argmax(scores))
                matched_word = active_seeds[matched_idx]

                # We flag the matched word as 'Responsible' for the frontend to highlight
                responsible_words.add(matched_word)

                results.append({
                    "clause_index": i,
                    "matched_anchor": matched_word,
                    "clarity_score": round(1.0 - max_score, 2),
                    "risk_level": "High" if max_score > 0.85 else "Medium"
                })

        return {"risks": results, "responsible_words": list(responsible_words)}