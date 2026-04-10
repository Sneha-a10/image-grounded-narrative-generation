from language_layer.language_layer_main import language_layer_pipeline
from unittest.mock import patch


def test_language_layer_output_structure():

    mock_response = """
    {
        "story_text": "A dog plays with a ball in a park.",
        "mentioned_entities": ["dog", "ball"],
        "mentioned_environment": ["park"],
        "inferred_emotion": "happy"
    }
    """

    input_data = {
        "image_id": "test_img",
        "caption": "A dog playing with a ball in a park",

        "signals": {
            "subject": "dog",
            "subject_type": "animal",
            "objects": ["ball"],
            "environment": ["park"],
            "action_state": "play",
            "emotion_hint": "happy"
        },

        "constraints": {
            "max_length": 50,
            "tone": "neutral",
            "perspective": "third_person",
            "allowed_emotion_inference": "limited",
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS"
            ]
        }
    }

    with patch("language_layer.language_layer_main.generate_story", return_value=mock_response):
        output = language_layer_pipeline(input_data)

    print(output)

    assert isinstance(output, dict)

    expected_keys = {
        "story_text",
        "mentioned_entities",
        "mentioned_environment",
        "inferred_emotion",
        "image_id"
    }

    assert set(output.keys()) == expected_keys

def test_language_layer_determinism():
    from unittest.mock import patch
    from language_layer.language_layer_main import language_layer_pipeline

    mock_response = """
    {
        "story_text": "A dog plays with a ball in a park.",
        "mentioned_entities": ["dog", "ball"],
        "mentioned_environment": ["park"],
        "inferred_emotion": "happy"
    }
    """

    input_data = {
        "image_id": "test_img",
        "caption": "A dog playing with a ball in a park",

        "signals": {
            "subject": "dog",
            "subject_type": "animal",
            "objects": ["ball"],
            "environment": ["park"],
            "action_state": "play",
            "emotion_hint": "happy"
        },

        "constraints": {
            "max_length": 50,
            "tone": "neutral",
            "perspective": "third_person",
            "allowed_emotion_inference": "limited",
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_OFF_IMAGE_LOCATIONS"
            ]
        }
    }

    with patch("language_layer.language_layer_main.generate_story", return_value=mock_response):
        output1 = language_layer_pipeline(input_data)

    with patch("language_layer.language_layer_main.generate_story", return_value=mock_response):
        output2 = language_layer_pipeline(input_data)

    print("Output 1:", output1)
    print("Output 2:", output2)

    assert output1 == output2