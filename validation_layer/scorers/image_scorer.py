import math

class ImageStoryScorer:

    def _normalize_vector(self, vec):
        norm = math.sqrt(sum(x*x for x in vec))
        if norm == 0:
            return vec
        return [x / norm for x in vec]

    def _mock_embedding_to_keywords(self, embedding):
        # VERY SIMPLE mock logic
        # convert numbers to pseudo "tokens"
        return set([f"feat_{int(abs(x)*10)}" for x in embedding])

    def _tokenize(self, text):
        return set(text.lower().split())

    def _similarity(self, set1, set2):
        if not set1 or not set2:
            return 0.0
        return len(set1 & set2) / math.sqrt(len(set1) * len(set2))

    def score(self, embedding_vector, story_text):

        if not embedding_vector or not story_text:
            return 0.0

        img_tokens = self._mock_embedding_to_keywords(embedding_vector)
        story_tokens = self._tokenize(story_text)

        score = self._similarity(img_tokens, story_tokens)

        return round(score, 3)