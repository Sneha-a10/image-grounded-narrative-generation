from validation_layer.scoring_pipeline.aggregator import ScoreAggregator

def test_aggregation():
    agg = ScoreAggregator()

    scores = {
        "image_score": 1.0,
        "caption_score": 1.0,
        "signal_score": 1.0
    }

    assert agg.aggregate(scores) == 1.0