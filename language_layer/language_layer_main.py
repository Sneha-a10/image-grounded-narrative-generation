import json
from .prompt_builder import build_prompt
from .generator import generate_story
from .parser import parse_output


def language_layer_pipeline(input_data):

    if "signals" not in input_data:
        raise ValueError("Signals missing — required for language layer")

    prompt = build_prompt(input_data)

    raw_output = generate_story(prompt)

    final_output = parse_output(
        raw_output,
        input_data["image_id"],
        input_data["signals"]
    )

    return final_output


if __name__ == "__main__":

    caption = input("Enter caption: ")

    tokens = caption.lower().split()

    input_data = {
    "image_id": "img_dynamic",
    "caption": caption,

    "signals": {   # ✅ ADD THIS
        "subject": "dog",
        "subject_type": "animal",
        "objects": ["ball"],
        "environment": ["park"],
        "action_state": "play",
        "emotion_hint": "happy"
    },

        "constraints": {...},
        "control_metadata": {...}
    }

    output = language_layer_pipeline(input_data)

    print("\n--- OUTPUT ---\n")
    print(output)

    # ✅ SAVE JSON FILE
    with open("output.json", "w") as f:
        json.dump(output, f, indent=4)

    print("\n✅ Output saved as output.json")