from app.ml.lawformer_handler import lawformer
from sentence_transformers import util
import torch


class VSMClassifier:
    """
    Classifies documents into scope-limited domains using Vector Space Modeling (VSM).
    """

    def __init__(self):
        # Domain-specific seeds derived from your research paper
        self.domain_seeds = {
            "Criminal Law": [
                "penalty", "violation", "drunk driving", "breath analyzer",
                "BAC limit", "traffic rules", "theft", "noise pollution"
            ],
            "Contract Law": [
                "rent agreement", "lease termination", "security deposit",
                "EMI", "collateral", "loan dispute", "consumer redressal"
            ],
            "Education Law": [
                "teacher appointment", "recruitment", "wage rules",
                "probation", "leave policy", "service statutes"
            ]
        }
        self.centroids = self._initialize_centroids()

    def _initialize_centroids(self):
        # Pre-calculates the average vector (centroid) for each legal domain
        centroids = {}
        for domain, seeds in self.domain_seeds.items():
            embeddings = lawformer.get_embeddings(seeds)
            centroids[domain] = torch.mean(embeddings, dim=0)
        return centroids

    def predict_domain(self, document_text: str):
        # 1. Generate vector representation for the whole document
        doc_embedding = lawformer.get_embeddings([document_text])

        # 2. Compare against domain centroids using Cosine Similarity
        scores = {}
        for domain, centroid in self.centroids.items():
            similarity = util.cos_sim(doc_embedding, centroid.unsqueeze(0))
            scores[domain] = float(similarity)

        # 3. Select the domain with the highest similarity score
        predicted_domain = max(scores, key=scores.get)

        return {
            "predicted_domain": predicted_domain,
            "confidence_scores": {k: round(v, 3) for k, v in scores.items()}
        }