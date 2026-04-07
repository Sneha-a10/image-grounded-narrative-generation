from validation_layer.constraint_check.constraint_checker import ConstraintChecker


def test_violation():
    checker = ConstraintChecker()

    story = "dog runs in park with tree"
    expected = ["dog", "park"]
    actual = ["dog", "park", "tree"]

    constraints = ["NO_NEW_ENTITIES"]

    result = checker.check(story, expected, actual, constraints)

    assert result["violation"] is True
    assert "NO_NEW_ENTITIES" in result["violations"]


def test_no_violation():
    checker = ConstraintChecker()

    story = "dog runs in park"
    expected = ["dog", "park"]
    actual = ["dog", "park"]

    constraints = ["NO_NEW_ENTITIES"]

    result = checker.check(story, expected, actual, constraints)

    assert result["violation"] is False
    assert result["violations"] == []