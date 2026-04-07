from validation_layer.scorers.caption_scorer import CaptionStoryScorer


def test_caption_scorer():
    scorer = CaptionStoryScorer()

    caption = "A fox and a rabbit are in a room"

    good_story = "A fox is holding a rabbit inside a room"
    bad_story = "A car is driving fast on a highway"

    good_score = scorer.score(caption, good_story)
    bad_score = scorer.score(caption, bad_story)

    print("GOOD:", good_score)
    print("BAD:", bad_score)

    assert 0 <= good_score <= 1
    assert 0 <= bad_score <= 1