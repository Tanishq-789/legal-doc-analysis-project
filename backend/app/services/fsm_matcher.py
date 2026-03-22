import re


class FSMMatcher:
    """
    Finite State Machine logic to identify structural 'Anchors' in Contracts.
    Focuses on deterministic legal patterns.
    """

    def __init__(self):
        # Define the states/anchors for the Contract Domain
        self.structural_states = {
            "TERMINATION": [r"termination\s+of\s+agreement", r"right\s+to\s+terminate", r"notice\s+period"],
            "INDEMNIFICATION": [r"hold\s+harmless", r"indemnify\s+and\s+defend", r"liability\s+for\s+loss"],
            "LIABILITY": [r"limitation\s+of\s+liability", r"maximum\s+aggregate", r"consequential\s+damages"],
            "FORCE MAJEURE": [r"acts\s+of\s+god", r"unforeseeable\s+circumstances", r"beyond\s+control"],
            "JURISDICTION": [r"governing\s+law", r"exclusive\s+jurisdiction", r"courts\s+of"]
        }

    def get_structural_anchors(self, text: str):
        """
        Scans text for the 'Responsible Words' that satisfy FSM state transitions.
        """
        text_lower = text.lower()
        responsible_words = []
        identified_risks = []

        for state, patterns in self.structural_states.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    # Capture the specific phrase as an anchor
                    found_phrase = match.group(0).capitalize()
                    responsible_words.append(found_phrase)

                    # Create a mock risk object for the structural anchor
                    identified_risks.append({
                        "clause_index": -1,  # Structural anchors often apply to the whole doc
                        "matched_anchor": state,
                        "clarity_score": 0.95,
                        "risk_level": "Medium"
                    })
                    break  # Move to next state once current one is satisfied

        return {
            "responsible_words": list(set(responsible_words)),
            "identified_risks": identified_risks
        }