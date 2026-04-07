from validation_layer.scoring_pipeline.decision_engine import DecisionEngine

def test_accept():
    dec = DecisionEngine()

    scores = {
        "image_score": 0.8,
        "caption_score": 0.8,
        "signal_score": 0.8
    }

    final = 0.8

    assert dec.decide(final, scores) == "ACCEPT"


def test_reject():
    dec = DecisionEngine()

    scores = {
        "image_score": 0.5,
        "caption_score": 0.8,
        "signal_score": 0.8
    }

    final = 0.7

    assert dec.decide(final, scores) == "REJECT"