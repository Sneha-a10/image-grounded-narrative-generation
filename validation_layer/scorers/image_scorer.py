import torch
import torch.nn.functional as F
from transformers import CLIPTokenizer, CLIPTextModel
import spacy


class ImageStoryScorer:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Only TEXT encoder (not full CLIP model)
        self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
        self.text_model = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)

        self.text_model.eval()
        
        # Load spaCy
        self.nlp = spacy.load("en_core_web_sm")

    def _get_text_embedding(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.text_model(**inputs)

        # Mean pooling
        embedding = outputs.last_hidden_state.mean(dim=1)

        return F.normalize(embedding, p=2, dim=-1)

    def score(self, image_embedding, story_text, signals):
        """
        image_embedding: list[float] OR tensor (from vision layer)
        story_text: string
        signals: dict with subjects, objects, environment
        """

        if image_embedding is None or not story_text or not signals:
            return {
                "similarity": 0.0,
                "match_score": 0.0
            }

        # --- IMAGE EMBEDDING ---
        image_embedding = torch.tensor(image_embedding, dtype=torch.float32).to(self.device)

        if image_embedding.dim() == 1:
            image_embedding = image_embedding.unsqueeze(0)

        image_embedding = F.normalize(image_embedding, p=2, dim=-1)

        # --- STORY EMBEDDING ---
        story_embedding = self._get_text_embedding(story_text)

        # --- GLOBAL SIMILARITY ---
        cosine_sim = (image_embedding * story_embedding).sum(dim=-1).item()
        similarity = (cosine_sim + 1) / 2  # normalize

        # --- ENTITY ALIGNMENT ---
        expected_entities = self._extract_expected_entities(signals)
        story_entities = self._extract_story_entities(story_text)

        match_score = self._compute_match_score(expected_entities, story_entities)

        # --- HALLUCINATION ---
        hallucination_rate = self._compute_hallucination_rate(
            expected_entities, story_entities
        )

        # --- FINAL SCORE ---
        image_score = (
            0.5 * similarity
            + 0.3 * match_score
            - 0.4 * hallucination_rate
        )

        # clamp to [0,1]
        image_score = max(0.0, min(1.0, image_score))

        return round(float(image_score), 3)

    def _extract_expected_entities(self, signals):
        entities = set()

        entities.update(signals.get("subjects", []))
        entities.update(signals.get("objects", []))
        entities.update(signals.get("environment", []))

        return set(e.lower() for e in entities)


    def _extract_story_entities(self, story_text):
        doc = self.nlp(story_text.lower())

        entities = set()

        for token in doc:
            if token.pos_ in {"NOUN", "PROPN"}:
                entities.add(token.lemma_)

        return entities


    def _compute_match_score(self, expected_entities, story_entities):
        if not expected_entities:
            return 0.0

        matched = expected_entities & story_entities

        return len(matched) / len(expected_entities)
    
    def _compute_hallucination_rate(self, expected_entities, story_entities):
        if not story_entities:
            return 0.0

        extra = story_entities - expected_entities

        return len(extra) / len(story_entities)