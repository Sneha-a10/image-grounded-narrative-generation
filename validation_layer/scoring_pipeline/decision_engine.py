class DecisionEngine:

    def decide(self, final_score, scores):

        if (
            final_score >= 0.75 and
            scores["image_score"] >= 0.6 and
            scores["caption_score"] >= 0.6 and
            scores["signal_score"] >= 0.6
        ):
            return "ACCEPT"

        return "REJECT"