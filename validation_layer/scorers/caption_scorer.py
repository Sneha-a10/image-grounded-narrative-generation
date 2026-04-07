import math

class CaptionStoryScorer:

    def _tokenize(self, text):
        return set(text.lower().split())

    def _cosine_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        
        if not set1 or not set2:
            return 0.0
        
        return intersection / math.sqrt(len(set1) * len(set2))

    def score(self, caption_text: str, story_text: str) -> float:

        if not caption_text or not story_text:
            return 0.0

        tokens1 = self._tokenize(caption_text)
        tokens2 = self._tokenize(story_text)

        score = self._cosine_similarity(tokens1, tokens2)

        return round(score, 3)