import re

class Preprocessor:
    def clean_legal_text(self, text: str):
        # 1. Remove noise but keep Latin phrases (e.g., 'inter alia')
        # 2. Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # 3. Handle specific legal characters (e.g., §)
        text = text.replace('§', 'Section')
        return text.strip()

cleaner = Preprocessor()