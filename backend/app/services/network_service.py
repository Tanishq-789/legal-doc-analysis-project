import re


class NetworkService:
    """
    Identifies document interdependencies by parsing section cross-references.
    """

    def build_dependency_graph(self, clauses: list[str]):
        nodes = []
        edges = []

        for i, text in enumerate(clauses):
            # Create a node for every clause
            nodes.append({"id": str(i), "data": {"label": f"Clause {i + 1}"}})

            # Look for references like 'Section 2' or 'Clause 5'
            refs = re.findall(r'(?:Section|Clause|Article)\s+(\d+)', text, re.I)
            for ref in refs:
                target_idx = int(ref) - 1
                if 0 <= target_idx < len(clauses) and target_idx != i:
                    edges.append({
                        "id": f"e{i}-{target_idx}",
                        "source": str(i),
                        "target": str(target_idx),
                        "animated": True
                    })

        return {"nodes": nodes, "edges": edges}