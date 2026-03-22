from app.ml.lawformer_handler import get_lawformer
import logging

# Standard logger for real-time inference tracking
logger = logging.getLogger("uvicorn.error")


class VSMClassifier:
    def __init__(self):
        # Lazy load the Lawformer singleton
        self.lawformer = get_lawformer()

        # Primary Domain Mapping
        self.labels = ["Contract Law", "Criminal Law", "Education Law"]

        # --- EDGE CASE GUARD ---
        # If no domain hits this threshold, it's considered 'General Legal'
        self.CONFIDENCE_THRESHOLD = 0.45

    def predict_domain(self, text: str):
        """
        Predicts the legal domain using a hybrid approach:
        1. Lawformer Transformer (Contextual Analysis)
        2. Domain-Specific Heuristics (Statutory/Academic weight adjustment)
        3. Confidence Thresholding (Edge case handling for unknown docs)
        """
        try:
            # 1. PREPROCESSING: Slice to the operative content zone
            # Most legal PDFs have headers; we focus on the core context (300-4300 chars)
            clean_text = text[300:4396] if len(text) > 500 else text

            # 2. TRANSFORMER INFERENCE
            result = self.lawformer.classify_with_evidence(clean_text)
            probs = result["probabilities"]
            evidence = result["responsible_words"]

            # 3. DOMAIN-SPECIFIC HEURISTICS (BOOSTING)
            header_zone = text[:800].upper()
            text_lower = text.lower()

            # Education Markers (University/Academic context)
            is_edu = any(k in header_zone for k in ["UNIVERSITY", "FACULTY", "ACADEMIC", "STUDENT", "SCHOOL"])
            # Criminal/Statutory Markers (Regulation/Offense context)
            is_crim = any(k in header_zone for k in ["ACT", "REGULATION", "PENALTY", "OFFENSE"])
            has_criminal_markers = any(k in text_lower for k in ["fine of", "impound", "imprisonment", "contravenes"])

            if is_edu:
                logger.info("--- [HEURISTIC] Education markers detected. Boosting Class 2 ---")
                probs[2] += 0.6
                probs[0] *= 0.2
                probs[1] *= 0.2
            elif is_crim or has_criminal_markers:
                logger.info("--- [HEURISTIC] Criminal/Statutory markers detected. Boosting Class 1 ---")
                probs[1] += 0.6
                probs[0] *= 0.2
                probs[2] *= 0.2

            # 4. NORMALIZATION
            # Ensure probabilities sum to 1.0 after heuristic adjustments
            total = sum(probs)
            probs = [p / total for p in probs]

            # 5. CONFIDENCE & THRESHOLD GUARD
            max_prob = max(probs)
            max_idx = probs.index(max_prob)

            # --- EDGE CASE: OUT-OF-DOMAIN HANDLING ---
            # If the best guess is still low-confidence, default to 'General Legal'
            if max_prob < self.CONFIDENCE_THRESHOLD:
                logger.warning(f"--- [GUARD] Low confidence ({round(max_prob, 4)}). Routing to General Fallback. ---")
                return {
                    "predicted_domain": "General Legal",
                    "confidence": round(max_prob, 4),
                    "probabilities": {self.labels[i]: round(probs[i], 4) for i in range(len(self.labels))},
                    "raw_evidence": evidence,
                    "is_unknown": True
                }

            # 6. FINAL SUCCESS PAYLOAD
            predicted_label = self.labels[max_idx]
            logger.info(f"--- [ML] Final Prediction: {predicted_label} ({round(max_prob, 4)}) ---")

            return {
                "predicted_domain": predicted_label,
                "confidence": round(max_prob, 4),
                "probabilities": {self.labels[i]: round(probs[i], 4) for i in range(len(self.labels))},
                "raw_evidence": evidence,
                "is_unknown": False
            }

        except Exception as e:
            logger.error(f"--- [ERROR] Classifier Pipeline Failed: {str(e)} ---")
            # Default fallback for catastrophic ML failures
            return {
                "predicted_domain": "General Legal",
                "confidence": 0.0,
                "error": str(e),
                "is_unknown": True
            }