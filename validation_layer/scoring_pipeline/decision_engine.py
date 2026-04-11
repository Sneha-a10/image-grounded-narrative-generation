class DecisionEngine:

    def decide(self, image_score, caption_score, signal_score, final_score):

        # ---- RELAXED THRESHOLDS ----

        if final_score >= 0.5:
            return "ACCEPT"

        # Optional: strong failure cases
        if image_score < 0.3:
            return "REJECT"

        if signal_score < 0.3:
            return "REJECT"

        return "REJECT"