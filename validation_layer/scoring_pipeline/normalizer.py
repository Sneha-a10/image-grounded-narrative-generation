class ScoreNormalizer:

    def normalize(self, image_score, caption_score, signal_score):

        def clamp(x):
            return max(0, min(1, x))

        return {
            "image_score": clamp(image_score),
            "caption_score": clamp(caption_score),
            "signal_score": clamp(signal_score)
        }