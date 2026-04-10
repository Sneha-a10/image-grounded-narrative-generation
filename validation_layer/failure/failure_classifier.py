class FailureClassifier:

    def classify(self, image_score, caption_score, signal_score, final_score):

        failures = []

        if image_score < 0.5:
            failures.append("image_misalignment")

        if caption_score < 0.5:
            failures.append("caption_misalignment")

        if signal_score < 0.4:
            failures.append("signal_violation")

        # --- DECISION ---
        if len(failures) == 1:
            return failures[0]

        if len(failures) > 1:
            return "multi_failure"

        return "no_failure"