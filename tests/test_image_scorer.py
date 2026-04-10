from validation_layer.scorers.image_scorer import ImageStoryScorer
import random


def test_image_scorer():
    scorer = ImageStoryScorer()

    # Mock embedding (simulate vision layer output)
    # So:
    # scores will NOT be meaningful yet
    # this is ONLY to verify pipeline works
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

    assert 0 <= good_result['similarity'] <= 1
    assert 0 <= good_result['match_score'] <= 1
    assert 0 <= bad_result['similarity'] <= 1
    assert 0 <= bad_result['match_score'] <= 1
    assert 0 <= hallucinated_result['similarity'] <= 1
    assert 0 <= hallucinated_result['match_score'] <= 1