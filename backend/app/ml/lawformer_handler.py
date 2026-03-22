from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import logging

# Initialize logger for tracking ML operations
logger = logging.getLogger("uvicorn.error")


class LawformerHandler:
    def __init__(self):
        """
        Initializes Lawformer with support for attention output.
        Enabling output_attentions=True is critical for identifying
        responsible words during visualization.
        """
        self.model_path = os.path.join(os.path.dirname(__file__), "model", "lawformer_final_model")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        logger.info(f"--- [INIT] Loading Lawformer from {self.model_path} on {self.device} ---")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path,
                local_files_only=True,
                output_hidden_states=True,
                output_attentions=True,  # REQUIRED: To extract responsible words
                use_safetensors=True
            ).to(self.device)
            logger.info("--- [SUCCESS] Lawformer Weights Materialized Successfully ---")
        except Exception as e:
            logger.error(f"--- [CRITICAL] Failed to load Lawformer: {str(e)} ---")
            raise e

        self.model.eval()

    def _generate_global_attention_mask(self, input_ids):
        """
        Generates the global attention mask required by Longformer/Lawformer architecture.
        Assigns global attention to the <s> token (index 0).
        """
        global_attention_mask = torch.zeros_like(input_ids)
        global_attention_mask[:, 0] = 1
        return global_attention_mask

    def get_embeddings(self, text_list: list[str]):
        """
        Generates semantic embeddings for document segments.
        Used for downstream VSM/Cosine Similarity tasks.
        """
        logger.info(f"--- [ML] Generating embeddings for {len(text_list)} items ---")
        inputs = self.tokenizer(
            text_list,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=4096
        ).to(self.device)

        inputs['global_attention_mask'] = self._generate_global_attention_mask(inputs['input_ids'])

        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use the CLS token embedding from the last hidden state
            embeddings = outputs.hidden_states[-1][:, 0, :]
        return embeddings

    def classify_with_evidence(self, text: str, top_k: int = 15):
        """
        Performs classification and extracts the tokens responsible for the decision.

        Args:
            text: Raw document text.
            top_k: Number of 'responsible words' to return for visualization.

        Returns:
            dict: Probabilities for each domain and a list of evidence tokens.
        """
        logger.info("--- [ML] Running Domain Classification with Evidence Extraction ---")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=4096,
            padding=True
        ).to(self.device)

        inputs['global_attention_mask'] = self._generate_global_attention_mask(inputs['input_ids'])

        with torch.no_grad():
            outputs = self.model(**inputs)

            # 1. Get Prediction Probabilities
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # 2. Extract Attention (Responsible Words)
            # We look at the last layer's attention [layer_index][batch][head][token][token]
            # Specifically, the attention the CLS token (index 0) pays to other tokens
            last_layer_attn = outputs.attentions[-1]
            avg_attention = last_layer_attn[0].mean(dim=0)  # Average across all attention heads
            cls_attention = avg_attention[0, :]  # Attention from <s> token to others

            # 3. Map attention back to tokens
            tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

            # Combine, filter special tokens, and sort by weight
            token_evidence = []
            for i, (token, score) in enumerate(zip(tokens, cls_attention.tolist())):
                # Filter out padding and special control tokens
                if token not in [self.tokenizer.pad_token, '<s>', '</s>', '<pad>'] and not token.startswith(' '):
                    # Remove the 'Ġ' (BPE space character) for cleaner visualization
                    clean_token = token.replace('Ġ', '').strip()
                    if len(clean_token) > 2:  # Ignore very short noise
                        token_evidence.append((clean_token, score))

            # Sort by attention score descending
            token_evidence.sort(key=lambda x: x[1], reverse=True)
            top_evidence = [t[0] for t in token_evidence[:top_k]]

        return {
            "probabilities": probs[0].tolist(),
            "responsible_words": top_evidence
        }


# --- Singleton Pattern for Lazy Loading ---
_lawformer_instance = None


def get_lawformer():
    global _lawformer_instance
    if _lawformer_instance is None:
        logger.info("--- [LAZY LOAD] Initializing Lawformer for the first time ---")
        _lawformer_instance = LawformerHandler()
    return _lawformer_instance