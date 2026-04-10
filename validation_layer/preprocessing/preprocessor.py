import re

class StoryPreprocessor:

    def process(self, story_text: str):

        if not isinstance(story_text, str) or not story_text:
            raise Exception("Invalid story_text")

        # 1. Lowercase
        text = story_text.lower()

        # 2. Sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # 3. Tokenization
        tokens = re.findall(r'\b\w+\b', text)

        return {
            "processed_text": " ".join(tokens),
            "tokens": tokens,
            "sentences": sentences
        }