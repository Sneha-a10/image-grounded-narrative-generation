from validation_layer.scorers.image_scorer import ImageStoryScorer

def test_basic_score():
    scorer = ImageStoryScorer()

    embedding = [0.1, 0.2, 0.3]
    story = "feat_1 feat_2 something"

    score = scorer.score(embedding, story)

    assert score > 0


def test_no_overlap():
    scorer = ImageStoryScorer()

    embedding = [0.9, 0.8]
    story = "completely unrelated words"

    score = scorer.score(embedding, story)

    assert score == 0


def test_empty_input():
    scorer = ImageStoryScorer()

    assert scorer.score([], "") == 0.0