import networkx as nx
import re
from collections import Counter


class TermSelector:
    """
    Calculates term value using Graph Centrality and optimizes selection via Knapsack.
    """

    def extract_dynamic_terms(self, text: str):
        # 1. Preprocessing: Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())  # Words > 4 chars
        if not words: return []

        # 2. Build Co-occurrence Graph
        G = nx.Graph()
        window_size = 3
        for i in range(len(words) - window_size):
            window = words[i:i + window_size]
            for u in window:
                for v in window:
                    if u != v:
                        G.add_edge(u, v)

        # 3. Calculate Degree Centrality as 'Value'
        centrality = nx.degree_centrality(G)

        # 4. Prepare for Knapsack
        # Weight = length of word (visual space); Value = centrality score * 100
        candidate_terms = []
        for word, score in centrality.items():
            candidate_terms.append({
                "text": word.capitalize(),
                "weight": len(word),
                "value": int(score * 1000)
            })
        return candidate_terms

    def optimize_word_cloud(self, term_data: list[dict], capacity: int = 150):
        # Greedy Knapsack approach based on Value/Weight ratio
        sorted_terms = sorted(term_data, key=lambda x: x['value'] / max(x['weight'], 1), reverse=True)
        selected, current_weight = [], 0
        for item in sorted_terms:
            if current_weight + item['weight'] <= capacity:
                selected.append(item)
                current_weight += item['weight']
        return selected