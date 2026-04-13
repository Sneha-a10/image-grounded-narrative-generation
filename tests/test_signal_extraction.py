from signal_extraction.extractor import SignalExtractor


def test_extractor_returns_correct_structure():
    extractor = SignalExtractor()

    caption = "A dog playing with a ball in a park"
    signals = extractor.extract(caption)

    assert isinstance(signals, dict)

    expected_keys = {
        "subject",
        "subject_type",
        "objects",
        "environment",
        "action_state",
        "emotion_hint",
        "attributes"
    }

    print("subject", signals["subject"])
    print("subject_type", signals["subject_type"])
    print("objects", signals["objects"])
    print("environment", signals["environment"])
    print("action_state", signals["action_state"])
    print("emotion_hint", signals["emotion_hint"])

    assert set(signals.keys()) == expected_keys


def test_full_signal_extraction():
    extractor = SignalExtractor()

    caption = "A happy dog playing with a ball in a park"
    signals = extractor.extract(caption)

    print("subject", signals["subject"])
    print("subject_type", signals["subject_type"])
    print("objects", signals["objects"])
    print("environment", signals["environment"])
    print("action_state", signals["action_state"])
    print("emotion_hint", signals["emotion_hint"])

    assert signals["subject"] in ["dog", "happy dog"]
    assert signals["subject_type"] == "animal"
    assert "ball" in signals["objects"]
    assert "park" in signals["environment"]
    assert signals["action_state"] == "play"
    assert signals["emotion_hint"] == "happy"
    assert "happy" in signals["attributes"]

def test_signal_types_and_constraints():
    extractor = SignalExtractor()

    caption = "A happy dog playing with a ball in a park"
    signals = extractor.extract(caption)

    print(signals)

    assert isinstance(signals["subject"], (str, type(None)))
    assert signals["subject_type"] in {"human", "animal", "object", None}

    assert isinstance(signals["objects"], list)
    assert all(isinstance(obj, str) for obj in signals["objects"])

    assert isinstance(signals["environment"], list)
    assert all(isinstance(env, str) for env in signals["environment"])

    assert isinstance(signals["action_state"], (str, type(None)))
    assert isinstance(signals["emotion_hint"], (str, type(None)))
    assert isinstance(signals["attributes"], list)

def test_multiword_extraction():
    extractor = SignalExtractor()

    caption = "A dog playing with a tennis ball in a city park"
    signals = extractor.extract(caption)

    print("objects", signals["objects"])
    print("environment", signals["environment"])

    assert "tennis ball" in signals["objects"]
    assert "city park" in signals["environment"]

def test_empty_caption():
    extractor = SignalExtractor()

    caption = ""
    signals = extractor.extract(caption)

    print(signals)

    assert signals["subject"] is None
    assert signals["objects"] == []
    assert signals["environment"] == []