import re
import nltk
from nltk.tokenize import sent_tokenize

# Ensure NLTK data is available for sentence splitting
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class ClauseSegmenter:
    def __init__(self, max_chars_per_node=800):
        # Improved pattern: capturing group ensures headers are KEPT in the output
        self.legal_pattern = r'((?m)^(?:Section|Article|Clause|RULE|CHAPTER)\s+\d+[\.:]?\s+)'
        self.max_chars = max_chars_per_node

    def segment(self, text: str) -> list[str]:
        # 1. Primary Pass: Statutory Regex Splitting
        # We use re.split with a capturing group to keep the headers
        parts = re.split(self.legal_pattern, text)

        # Re-merge headers with their following content
        clauses = []
        if len(parts) > 1:
            # If parts[0] is empty, it means the doc started with a header
            start_idx = 1 if not parts[0].strip() else 0
            for i in range(start_idx, len(parts), 2):
                header = parts[i] if i < len(parts) else ""
                content = parts[i + 1] if i + 1 < len(parts) else ""
                clauses.append((header + content).strip())
        else:
            clauses = [text.strip()]

        # 2. Secondary Pass: Recursive Granularity Check
        # If any clause is still too dense (like your research paper), split by sentences
        final_segments = []
        for clause in clauses:
            if len(clause) > self.max_chars:
                final_segments.extend(self._sub_segment(clause))
            else:
                final_segments.append(clause)

        return [s for s in final_segments if len(s) > 30]

    def _sub_segment(self, text: str) -> list[str]:
        """
        Groups sentences into chunks that respect the 'max_chars' limit.
        This prevents the 'one-giant-node' issue in FSM visualizations.
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""

        for sent in sentences:
            if len(current_chunk) + len(sent) < self.max_chars:
                current_chunk += " " + sent
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sent

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks