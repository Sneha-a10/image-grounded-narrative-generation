from validation_layer.scorers.image_scorer import ImageStoryScorer
import random


def test_image_scorer():
    scorer = ImageStoryScorer()

    image_embedding = [random.uniform(-1, 1) for _ in range(512)]

    signals = {
        "subjects": ["fox"],
        "objects": ["rabbit"],
        "environment": ["room"]
    }

    good_story = "A fox gently holds a rabbit in a room"
    bad_story = "A car drives fast on a highway"
    hallucinated_story = "A fox holds a rabbit while a dragon watches in a room"

    good_result = scorer.score(image_embedding, good_story, signals)
    bad_result = scorer.score(image_embedding, bad_story, signals)
    hallucinated_result = scorer.score(image_embedding, hallucinated_story, signals)

    print("GOOD:", good_result)
    print("BAD:", bad_result)
    print("HALLUCINATED:", hallucinated_result)

    # TYPE CHECK
    assert isinstance(good_result, float)
    assert isinstance(bad_result, float)
    assert isinstance(hallucinated_result, float)

    # RANGE CHECK
    assert 0 <= good_result <= 1
    assert 0 <= bad_result <= 1
    assert 0 <= hallucinated_result <= 1