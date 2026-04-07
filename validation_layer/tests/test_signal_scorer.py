from validation_layer.scorers.signal_scorer import SignalConsistencyEvaluator

def test_perfect_match():
    scorer = SignalConsistencyEvaluator()

    expected = {
        "subjects": ["dog"],
        "objects": ["ball"],
        "environment": ["park"],
        "actions": ["running"]
    }

    actual = {
        "subjects": ["dog"],
        "objects": ["ball"],
        "environment": ["park"],
        "actions": ["running"]
    }

    score = scorer.evaluate(expected, actual)

    assert score == 1.0


def test_with_hallucination():
    scorer = SignalConsistencyEvaluator()

    expected = {
        "subjects": ["dog"],
        "objects": ["ball"],
        "environment": ["park"],
        "actions": ["running"]
    }

    actual = {
        "subjects": ["dog"],
        "objects": ["ball", "tree"],  # extra
        "environment": ["park"],
        "actions": ["running"]
    }

    score = scorer.evaluate(expected, actual)

    assert score < 1.0


def test_missing_entities():
    scorer = SignalConsistencyEvaluator()

    expected = {
        "subjects": ["dog"],
        "objects": ["ball"],
        "environment": ["park"],
        "actions": ["running"]
    }

    actual = {
        "subjects": ["dog"],
        "objects": [],
        "environment": ["park"],
        "actions": []
    }

    score = scorer.evaluate(expected, actual)

    assert score < 1.0


def test_empty_input():
    scorer = SignalConsistencyEvaluator()

    score = scorer.evaluate({}, {})

    assert score == 0