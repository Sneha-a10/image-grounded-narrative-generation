from validation_layer.scorers.caption_scorer import CaptionStoryScorer

def test_high_similarity():
    scorer = CaptionStoryScorer()

    caption = "dog playing in park"
    story = "dog is playing in the park happily"

    score = scorer.score(caption, story)

    assert score > 0.5


def test_low_similarity():
    scorer = CaptionStoryScorer()

    caption = "dog in park"
    story = "a car is driving on the road"

    score = scorer.score(caption, story)

    assert score < 0.3


def test_empty_input():
    scorer = CaptionStoryScorer()

    assert scorer.score("", "") == 0.0