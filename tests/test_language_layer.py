import sys
sys.path.append(".")

from language_layer.language_layer_main import language_layer_pipeline

def test_language_layer():

    input_data = {
        "image_id": "img_test",

        "caption": "A dog playing with a ball in a park",

        "signals": {
            "subject": "dog",
            "objects": ["ball"],
            "environment": ["park"],
            "action_state": "playing",
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

    print("\n--- RUNNING LANGUAGE LAYER ---\n")

    output = language_layer_pipeline(input_data)

    print("\n--- GENERATED OUTPUT ---\n")
    print(output)

    if "story_text" in output:
        print("\n✅ FINAL STORY:\n")
        print(output["story_text"])
    else:
        print("\n❌ GENERATION FAILED\n")


if __name__ == "__main__":
    test_language_layer()