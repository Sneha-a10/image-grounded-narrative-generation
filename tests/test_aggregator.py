from validation_layer.scoring_pipeline.aggregator import ScoreAggregator


def test_score_aggregator():
    agg = ScoreAggregator()

    # GOOD CASE
    good = agg.aggregate(0.56, 0.93, 0.5)

    # HALLUCINATED CASE
    hallucinated = agg.aggregate(0.47, 0.85, 0.25)

    # BAD CASE
    bad = agg.aggregate(0.0, 0.5, 0.0)

    print("GOOD:", good)
    print("HALLUCINATED:", hallucinated)
    print("BAD:", bad)

    assert 0 <= good <= 1
    assert 0 <= hallucinated <= 1
    assert 0 <= bad <= 1