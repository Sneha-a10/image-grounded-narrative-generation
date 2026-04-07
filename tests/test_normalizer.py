from validation_layer.scoring_pipeline.normalizer import ScoreNormalizer

def test_clamping():
    norm = ScoreNormalizer()

    result = norm.normalize(1.2, -0.5, 0.8)

    assert result["image_score"] == 1
    assert result["caption_score"] == 0
    assert result["signal_score"] == 0.8