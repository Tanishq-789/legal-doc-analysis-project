import networkx as nx
import re


class TermSelector:
    """
    Implements VSM (Vector Space Model) weights via Graph Centrality
    and FSM (Finite State Machine) logic for structural anchoring.
    """

    def __init__(self):
        # Structural anchors for Contract Law (FSM Logic)
        self.contract_patterns = [
            r"TERMINATION", r"INDEMNIFICATION", r"LIABILITY", r"FORCE MAJEURE",
            r"GOVERNING LAW", r"CONFIDENTIALITY", r"INTELLECTUAL PROPERTY"
        ]
        # High-weight terms for Criminal Law (VSM Logic)
        self.criminal_keywords = {
            'felony', 'indictment', 'misdemeanor', 'prosecution', 'statute',
            'custody', 'defendant', 'allegation', 'offense', 'testimony'
        }

    def extract_responsible_terms(self, text: str, domain: str):
        """
        Selects words based on domain-specific algorithms (VSM/FSM).
        """
        responsible_words = []
        text_upper = text.upper()

        if domain == "Contract Law":
            # FSM-style structural search
            for pattern in self.contract_patterns:
                if re.search(r'\b' + pattern + r'\b', text_upper):
                    responsible_words.append(pattern.capitalize())

        elif domain == "Criminal Law":
            # VSM-style keyword weighting
            words = re.findall(r'\b\w{4,}\b', text.lower())
            for word in words:
                if word in self.criminal_keywords:
                    responsible_words.append(word.capitalize())

        return list(set(responsible_words))

    def extract_dynamic_terms(self, text: str):
        """
        Builds a co-occurrence graph (VSM methodology) to find central terms.
        """
        words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
        if not words: return []

        G = nx.Graph()
        for i in range(len(words) - 3):
            window = words[i:i + 3]
            for u in window:
                for v in window:
                    if u != v: G.add_edge(u, v)

        centrality = nx.degree_centrality(G)
        return [{"text": w.capitalize(), "weight": len(w), "value": int(s * 1000)}
                for w, s in centrality.items()]

    def optimize_word_cloud(self, term_data: list[dict], priority_terms: list[str], capacity: int = 250):
        """
        Knapsack Optimization: Prioritizes 'Responsible Words' identified
        by Lawformer/VSM/FSM to be visual focus points.
        """
        # Boost value of priority terms so they 'win' the knapsack spot
        for item in term_data:
            if item['text'] in [p.capitalize() for p in priority_terms]:
                item['value'] *= 5  # Heavily weight the responsible words

        # Greedy selection based on Value Density
        sorted_terms = sorted(term_data, key=lambda x: x['value'] / max(x['weight'], 1), reverse=True)

        selected, current_weight = [], 0
        for item in sorted_terms:
            if current_weight + item['weight'] <= capacity:
                selected.append(item)
                current_weight += item['weight']

        return selected[:35]  # Best 35 for UI clarity