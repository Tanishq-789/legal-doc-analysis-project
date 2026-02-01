from sentence_transformers import SentenceTransformer
import torch

class LawformerHandler:
    def __init__(self):
        # Using a legal-specific BERT variant optimized for semantic understanding
        self.model_name = 'nlpaueb/legal-bert-base-uncased'
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(self.model_name, device=self.device)

    def get_embeddings(self, text_list: list[str]):
        """Generates contextual embeddings for legal clauses."""
        return self.model.encode(text_list, convert_to_tensor=True)

# Singleton instance
lawformer = LawformerHandler()