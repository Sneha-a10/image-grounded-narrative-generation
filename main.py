import json
from prompt_builder import build_prompt
from generator import generate_story
from parser import parse_output


def language_layer_pipeline(input_data):

    prompt = build_prompt(input_data)

    raw_output = generate_story(prompt)

    final_output = parse_output(raw_output, input_data["image_id"])

    return final_output


if __name__ == "__main__":

    caption = input("Enter caption: ")

    tokens = caption.lower().split()

    input_data = {
        "image_id": "img_dynamic",
        "caption_data": {
            "caption_text": caption,
            "tokens": tokens
        },
        "constraints": {
            "max_length": 120,
            "tone": "neutral_descriptive",
            "perspective": "third_person",
            "allowed_emotion_inference": "limited",
            "negative_rules": [
                "NO_NEW_ENTITIES",
                "NO_INTERNAL_THOUGHTS",
                "NO_OFF_IMAGE_LOCATIONS",
                "NO_TEMPORAL_JUMPS"
            ]
        },
        "control_metadata": {
            "preset_family": "manual",
            "preset_level": 0,
            "trigger_reason": "user_input"
        }
    }

    output = language_layer_pipeline(input_data)

    print("\n--- OUTPUT ---\n")
    print(output)

    # ✅ SAVE JSON FILE
    with open("output.json", "w") as f:
        json.dump(output, f, indent=4)

    print("\n✅ Output saved as output.json")