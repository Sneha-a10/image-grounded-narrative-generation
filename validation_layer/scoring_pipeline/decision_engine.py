class DecisionEngine:

    def decide(self, image_score, caption_score, signal_score, final_score):

        if (
            final_score >= 0.6
            and image_score >= 0.5
            and caption_score >= 0.5
            and signal_score >= 0.4
        ):
            return "ACCEPT"

        return "REJECT"