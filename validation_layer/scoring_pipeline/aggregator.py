class ScoreAggregator:

    def aggregate(self, image_score, caption_score, signal_score):
        """
        All inputs must be in [0,1]
        """

        final_score = (
            0.5 * image_score
            + 0.25 * caption_score
            + 0.25 * signal_score
        )

        return round(final_score, 3)