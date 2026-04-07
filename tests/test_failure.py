from validation_layer.failure.failure_classifier import FailureClassifier

def test_constraint_priority():
    fc = FailureClassifier()

    result = fc.classify(
        {"image_score": 0.9, "caption_score": 0.9, "signal_score": 0.9},
        True
    )

    assert result == "constraint_violation"


def test_single_failure():
    fc = FailureClassifier()

    result = fc.classify(
        {"image_score": 0.5, "caption_score": 0.9, "signal_score": 0.9},
        False
    )

    assert result == "image_misalignment"