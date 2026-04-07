from validation_layer.input_validator.validator import InputValidator

validator = InputValidator()


def test_valid_input():
    data = {
        "image_id": "img_1",
        "caption_data": {"caption_text": "A dog in a park"},
        "visual_features": {"embedding_vector": [0.1, 0.2]},
        "generation_output": {
            "story_text": "A dog runs in a park",
            "sentences": ["A dog runs in a park"],
            "word_count": 6
        },
        "signal_extraction": {
            "semantic_signals": {
                "subjects": ["dog"],
                "objects": [],
                "environment": ["park"],
                "actions": ["running"],
                "attributes": []
            }
        },
        "constraints": {
            "negative_rules": ["NO_NEW_ENTITIES"]
        }
    }

    assert validator.validate(data) is False 


def test_missing_field():
    data = {}
    assert validator.validate(data) is False


def test_wrong_type():
    data = {
        "image_id": 123
    }
    assert validator.validate(data) is False


def test_empty_story():
    data = {
        "image_id": "img_1",
        "caption_data": {"caption_text": ""},
        "visual_features": {"embedding_vector": [0.1]},
        "generation_output": {
            "story_text": "",
            "sentences": [],
            "word_count": 0
        },
        "signal_extraction": {
            "semantic_signals": {
                "subjects": [],
                "objects": [],
                "environment": [],
                "actions": [],
                "attributes": []
            }
        },
        "constraints": {
            "negative_rules": []
        }
    }

    assert validator.validate(data) is False

def test_fully_valid_input():
    data = {
        "image_id": "img_1",
        "caption_data": {"caption_text": "A dog in a park"},
        "visual_features": {"embedding_vector": [0.1, 0.2]},
        "generation_output": {
            "story_text": "A dog runs in a park happily",
            "sentences": ["A dog runs in a park happily"],
            "word_count": 7
        },
        "signal_extraction": {
            "semantic_signals": {
                "subjects": ["dog"],
                "objects": ["ball"],
                "environment": ["park"],
                "actions": ["running"],
                "attributes": ["happy"]
            }
        },
        "constraints": {
            "negative_rules": ["NO_NEW_ENTITIES"]
        }
    }

    assert validator.validate(data) is True