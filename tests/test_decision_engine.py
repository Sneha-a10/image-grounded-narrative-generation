from validation_layer.scoring_pipeline.decision_engine import DecisionEngine


def test_decision_engine():
    engine = DecisionEngine()

    # GOOD
    result_good = engine.decide(
        image_score=0.56,
        caption_score=0.93,
        signal_score=0.5,
        final_score=0.638
    )

    # HALLUCINATED
    result_hallucinated = engine.decide(
        image_score=0.47,
        caption_score=0.85,
        signal_score=0.25,
        final_score=0.51
    )

    # BAD
    result_bad = engine.decide(
        image_score=0.0,
        caption_score=0.5,
        signal_score=0.0,
        final_score=0.125
    )

    print("GOOD:", result_good)
    print("HALLUCINATED:", result_hallucinated)
    print("BAD:", result_bad)

    assert result_good == "ACCEPT"
    assert result_hallucinated == "REJECT"
    assert result_bad == "REJECT"