import re


class ClauseSegmenter:
    """
    Segments legal text into distinct clauses using pattern recognition.
    Identifies common legal structures like 'Section 1', 'Article II', etc.
    """

    def __init__(self):
        # Regex to identify common legal list and section headers
        self.section_pattern = r'(?m)^(?:Section|Article|Clause)\s+\d+[\.:]?\s+.*$'
        self.list_pattern = r'\n\s*\(?[a-z0-9]\)\s+'

    def segment(self, text: str) -> list[str]:
        # First, split by major section headers
        sections = re.split(self.section_pattern, text)

        # Further refine segments by removing empty strings and whitespace
        clauses = [s.strip() for s in sections if len(s.strip()) > 20]

        # If the document is small/flat, split by paragraphs
        if len(clauses) <= 1:
            clauses = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 10]

        return clauses