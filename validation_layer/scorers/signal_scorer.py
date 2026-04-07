import spacy


class SignalConsistencyScorer:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def _extract_story_signals(self, story_text):
        doc = self.nlp(story_text.lower())

        signals = set()

        for token in doc:
            if token.pos_ in {"NOUN", "PROPN"}:
                signals.add(token.lemma_)

        return signals

    def _extract_expected_signals(self, signals):
        expected = set()

        expected.update(signals.get("subjects", []))
        expected.update(signals.get("objects", []))
        expected.update(signals.get("environment", []))
        expected.update(signals.get("actions", []))

        return set(s.lower() for s in expected)

    def score(self, expected_signals, story_text):

        if not expected_signals or not story_text:
            return 0.0

        expected = self._extract_expected_signals(expected_signals)
        story = self._extract_story_signals(story_text)

        if not expected:
            return 0.0

        # --- MATCH ---
        matched = expected & story
        match_score = len(matched) / len(expected)

        # --- MISSING ---
        missing = expected - story
        missing_rate = len(missing) / len(expected)

        # --- HALLUCINATION ---
        if not story:
            hallucination_rate = 0.0
        else:
            extra = story - expected
            hallucination_rate = len(extra) / len(story)

        # --- FINAL RAW SCORE ---
        score = match_score - hallucination_rate - missing_rate

        # clamp to [0,1]
        score = max(0.0, min(1.0, score))

        return round(score, 3)