import spacy


class SignalExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        self.EMOTION_WORDS = {
            "happy", "sad", "angry", "excited", "scared", "fearful",
            "nervous", "calm", "peaceful", "tired", "lonely",
            "joyful", "frustrated", "worried", "surprised"
        }

        self.ANIMAL_WORDS = {"dog", "cat", "horse", "bird"}

    def get_noun_chunk(self, token, doc):
        for chunk in doc.noun_chunks:
            if token in chunk:
                # remove determiners + use lemma
                words = [
                    t.lemma_ if t.pos_ in ("NOUN", "PROPN") else t.text
                    for t in chunk if t.dep_ != "det"
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
                "emotion_hint": None
            }

        # SUBJECT
        subject = None
        for token in doc:
            if token.dep_ in ("nsubj", "nsubjpass"):
                subject = token.lemma_
                break

        if subject is None:
            for token in doc:
                if token.pos_ in ("NOUN", "PROPN"):
                    subject = token.lemma_
                    break

        # SUBJECT TYPE
        subject_type = "object"
        if subject:
            for token in doc:
                if token.text == subject:
                    if token.ent_type_ == "PERSON":
                        subject_type = "human"
                    elif token.text.lower() in self.ANIMAL_WORDS:
                        subject_type = "animal"

        # ENVIRONMENT
        environment = []
        for token in doc:
            if token.dep_ == "pobj" and token.head.text in ("in", "on", "at", "under", "inside"):
                phrase = self.get_noun_chunk(token, doc)
                environment.append(phrase)

        # OBJECTS (exclude environment)
        objects = []
        for token in doc:
            if token.dep_ in ("dobj", "pobj"):
                phrase = self.get_noun_chunk(token, doc)
                if phrase not in environment:
                    objects.append(phrase)

        # ACTION STATE
        action_state = None
        for token in doc:
            if token.pos_ == "VERB":
                action_state = token.lemma_
                break

        # EMOTION
        emotion_hint = None
        for token in doc:
            if token.pos_ == "ADJ" and token.text.lower() in self.EMOTION_WORDS:
                emotion_hint = token.text.lower()
                break

        signals = {
            "subject": subject,
            "subject_type": subject_type,
            "objects": sorted(set(objects)),
            "environment": sorted(set(environment)),
            "action_state": action_state,
            "emotion_hint": emotion_hint
        }

        return signals