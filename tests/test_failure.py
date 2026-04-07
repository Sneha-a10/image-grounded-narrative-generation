from validation_layer.failure.failure_classifier import FailureClassifier

def test_failure_classifier():
    clf = FailureClassifier()

    # GOOD
    good = clf.classify(0.56, 0.93, 0.5, 0.638)

    # IMAGE FAIL
    image_fail = clf.classify(0.3, 0.8, 0.5, 0.55)

    # SIGNAL FAIL
    signal_fail = clf.classify(0.6, 0.8, 0.2, 0.5)

    # MULTI FAIL
    multi = clf.classify(0.3, 0.3, 0.2, 0.2)

    print("GOOD:", good)
    print("IMAGE_FAIL:", image_fail)
    print("SIGNAL_FAIL:", signal_fail)
    print("MULTI:", multi)

    assert good == "no_failure"
    assert image_fail == "image_misalignment"
    assert signal_fail == "signal_violation"
    assert multi == "multi_failure"