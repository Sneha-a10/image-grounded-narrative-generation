class FailureClassifier:

    def classify(self, scores, constraint_violation):

        if constraint_violation:
            return "constraint_violation"

        failures = []

        if scores["image_score"] < 0.6:
            failures.append("image_misalignment")

        if scores["caption_score"] < 0.6:
            failures.append("caption_misalignment")

        if scores["signal_score"] < 0.6:
            failures.append("signal_violation")

        if len(failures) == 1:
            return failures[0]

        return "multi_failure"