from app.services.fuzzy_detector import FuzzyDetector
from app.services.term_selector import TermSelector
from app.services.fsm_matcher import FSMMatcher
import logging

# Standard logger for orchestration tracking
logger = logging.getLogger("uvicorn.error")

class DomainRouter:
    def __init__(self):
        # Initialize specialized sub-services
        self.fuzzy_service = FuzzyDetector()
        self.vsm_service = TermSelector()
        self.fsm_service = FSMMatcher()

    async def route_and_analyze(self, domain: str, text: str):
        """
        The 'Pivot' Logic: Maps Lawformer's domain prediction to the
        appropriate specialized algorithm.
        Now includes a 'Graceful Fallback' for General Legal documents.
        """
        logger.info(f"--- [ROUTER] Routing based on domain: {domain} ---")

        # Case 1: Contract Law -> Uses FSM for structural anchoring
        if domain == "Contract Law":
            logger.info("--- [FLOW] Applying FSM (Finite State Machine) Analysis ---")
            analysis = self.fsm_service.get_structural_anchors(text)
            return {
                "algorithm": "FSM-Structural-Matcher",
                "responsible_words": analysis["responsible_words"],
                "identified_risks": analysis["identified_risks"]
            }

        # Case 2: Education Law -> Uses Fuzzy Semantic matching for institutions
        elif domain == "Education Law":
            logger.info("--- [FLOW] Applying Fuzzy Semantic Analysis ---")
            # Process text block for seed-based word extraction
            analysis = await self.fuzzy_service.identify_risks([text], domain=domain)
            return {
                "algorithm": "Fuzzy-Seed-Detector",
                "responsible_words": analysis["responsible_words"],
                "identified_risks": analysis["risks"]
            }

        # Case 3: Criminal Law -> Uses VSM for keyword weighting
        elif domain == "Criminal Law":
            logger.info("--- [FLOW] Applying VSM (Vector Space Model) Analysis ---")
            responsible_words = self.vsm_service.extract_responsible_terms(text, domain)
            return {
                "algorithm": "VSM-Graph-Centrality",
                "responsible_words": responsible_words,
                "identified_risks": []
            }

        # Case 4: General Legal / Fallback -> Handles 'Unknown' or low-confidence docs
        else:
            logger.info(f"--- [FLOW] Applying General Fallback Analysis for {domain} ---")
            # We return a generic configuration so the UI defaults to a Word Cloud
            return {
                "algorithm": "Keyword-Density-Analyzer",
                "responsible_words": [], # No specific domain-anchors to highlight
                "identified_risks": []
            }