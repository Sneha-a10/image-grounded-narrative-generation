from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class CaptionStoryScorer:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def score(self, caption, story_text):
        """
        caption: string
        story_text: string
        """

        if not caption or not story_text:
            return 0.0

        # Encode both texts
        embeddings = self.model.encode([caption, story_text])

        caption_emb = embeddings[0]
        story_emb = embeddings[1]

        # Cosine similarity
        cosine_sim = cosine_similarity(
            [caption_emb],
            [story_emb]
        )[0][0]

        # Normalize to [0,1]
        score = (cosine_sim + 1) / 2

        return round(float(score), 3)