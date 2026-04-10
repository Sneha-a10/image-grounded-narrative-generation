from validation_layer.scorers.signal_scorer import SignalConsistencyScorer


def test_signal_scorer():
    scorer = SignalConsistencyScorer()

    signals = {
        "subjects": ["fox"],
        "objects": ["rabbit"],
        "environment": ["room"],
        "actions": ["hold"]
    }

    good_story = "A fox holds a rabbit in a room"
    missing_story = "A fox is sitting"
    hallucinated_story = "A fox holds a rabbit while a dragon watches in a room"
    bad_story = "A car is driving on a highway"

    print("GOOD:", scorer.score(signals, good_story))
    print("MISSING:", scorer.score(signals, missing_story))
    print("HALLUCINATED:", scorer.score(signals, hallucinated_story))
    print("BAD:", scorer.score(signals, bad_story))