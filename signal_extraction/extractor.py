import spacy


class SignalExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        self.EMOTION_WORDS = {
            "happy", "sad", "angry", "excited", "scared", "fearful",
            "nervous", "calm", "peaceful", "tired", "lonely",
            "joyful", "frustrated", "worried", "surprised"
        }

        self.ANIMAL_WORDS = {
            "dog", "cat", "horse", "bird", "lion", "tiger", "bear",
            "rabbit", "hamster", "fish", "elephant", "giraffe", "cow", "pig", "sheep"
        }

        self.ENV_PREPOSITIONS = {
            "in", "on", "at", "under", "inside", "from", "through",
            "behind", "near", "beside", "outside", "against", "above", "below"
        }

    def get_noun_chunk(self, token, doc):
        for chunk in doc.noun_chunks:
            if token in chunk:
                # Use the chunk text but normalize it: remove determiners
                words = [
                    t.text for t in chunk if t.dep_ != "det"
                ]
                return " ".join(words)
        return token.lemma_

    def extract(self, caption: str) -> dict:
        doc = self.nlp(caption)

        if not caption or not caption.strip():
            return {
                "subject": None,
                "subject_type": None,
                "objects": [],
                "environment": [],
                "action_state": None,
                "emotion_hint": None,
                "attributes": []
            }

        # 1. SUBJECT
        subject = None
        subject_type = "object"

        # Search for animals/humans in noun chunks first (higher priority than grammar)
        for chunk in doc.noun_chunks:
            is_animal = any(t.lemma_.lower() in self.ANIMAL_WORDS for t in chunk)
            is_human = any(t.ent_type_ == "PERSON" or t.lemma_.lower() in ["man", "woman", "boy", "girl", "person"] for t in chunk)
            
            if is_animal or is_human:
                subject = self.get_noun_chunk(chunk.root, doc)
                subject_type = "animal" if is_animal else "human"
                break

        # Fallback to nsubj
        if subject is None:
            for token in doc:
                if token.dep_ in ("nsubj", "nsubjpass"):
                    subject = self.get_noun_chunk(token, doc)
                    if token.ent_type_ == "PERSON" or token.lemma_.lower() in ["man", "woman", "boy", "girl", "person"]:
                        subject_type = "human"
                    elif token.lemma_.lower() in self.ANIMAL_WORDS:
                        subject_type = "animal"
                    break

        # Fallback to first noun
        if subject is None:
            for token in doc:
                if token.pos_ in ("NOUN", "PROPN"):
                    subject = self.get_noun_chunk(token, doc)
                    break

        # 2. ENVIRONMENT
        environment = []
        for token in doc:
            if token.dep_ == "pobj" and token.head.text.lower() in self.ENV_PREPOSITIONS:
                # Check if it's likely an environment (e.g., place) or just an object
                phrase = self.get_noun_chunk(token, doc)
                environment.append(phrase)

        # 3. OBJECTS (exclude subject and environment)
        objects = []
        for token in doc:
            if token.dep_ in ("dobj", "pobj"):
                phrase = self.get_noun_chunk(token, doc)
                if phrase not in environment and (subject is None or phrase not in subject):
                    objects.append(phrase)

        # 4. ACTION STATE
        # Look for the main verb or any descriptive verb/participle
        actions = []
        for token in doc:
            if token.pos_ == "VERB" and token.pos_ != "AUX":
                actions.append(token.lemma_)
        
        action_state = actions[0] if actions else None

        # 5. EMOTION
        emotion_hint = None
        for token in doc:
            if token.pos_ == "ADJ" and token.text.lower() in self.EMOTION_WORDS:
                emotion_hint = token.text.lower()
                break

        # 6. ATTRIBUTES (descriptive adjectives like colors)
        attributes = []
        for token in doc:
            if token.pos_ == "ADJ" and token.text.lower() not in self.EMOTION_WORDS:
                # Avoid common non-descriptive adjectives if possible, but for now capture all
                attributes.append(token.text.lower())

        signals = {
            "subject": subject,
            "subject_type": subject_type,
            "actions": sorted(set(actions)),
            "objects": sorted(set(objects)),
            "environment": sorted(set(environment)),
            "attributes": sorted(set(attributes + ([emotion_hint] if emotion_hint else []))),
            "emotion_hint": emotion_hint,
            "action_state": actions[0] if actions else None
        }

        return signals