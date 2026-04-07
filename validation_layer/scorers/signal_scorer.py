class SignalConsistencyEvaluator:

    def _compute_match(self, expected, actual):
        if not expected:
            return 0

        matches = len(set(expected) & set(actual))
        return matches / len(expected)

    def _hallucination_rate(self, expected, actual):
        extra = set(actual) - set(expected)
        if not actual:
            return 0
        return len(extra) / len(actual)

    def _missing_rate(self, expected, actual):
        missing = set(expected) - set(actual)
        if not expected:
            return 0
        return len(missing) / len(expected)

    def evaluate(self, expected_signals, actual_signals):

        weights = {
            "subjects": 0.3,
            "objects": 0.3,
            "environment": 0.2,
            "actions": 0.2
        }

        match_score = 0
        hallucination = 0
        missing = 0

        for key, weight in weights.items():
            exp = expected_signals.get(key, [])
            act = actual_signals.get(key, [])

            match_score += weight * self._compute_match(exp, act)
            hallucination += weight * self._hallucination_rate(exp, act)
            missing += weight * self._missing_rate(exp, act)

        raw_score = match_score - hallucination - missing

        return max(0, min(1, round(raw_score, 3)))