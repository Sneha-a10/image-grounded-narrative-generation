class ScoreAggregator:

    def aggregate(self, scores):

        image = scores["image_score"]
        caption = scores["caption_score"]
        signal = scores["signal_score"]

        final = (
            0.5 * image +
            0.25 * caption +
            0.25 * signal
        )

        return round(final, 3)