from validation_layer.preprocessing.preprocessor import StoryPreprocessor

pre = StoryPreprocessor()


def test_basic_processing():
    text = "The Dog is Running in the Park."
    result = pre.process(text)

    assert result["processed_text"] == "the dog is running in the park"
    assert result["tokens"] == ["the", "dog", "is", "running", "in", "the", "park"]
    assert result["sentences"] == ["the dog is running in the park"]


def test_multiple_sentences():
    text = "A dog runs. It plays with a ball."
    result = pre.process(text)

    assert len(result["sentences"]) == 2


def test_invalid_input():
    try:
        pre.process("")
        assert False
    except:
        assert True