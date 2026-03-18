from preset_loader import load_presets, get_constraints
from prompt_builder import build_prompt
from generator import generate_story
from parser import parse_output


def language_layer_pipeline(input_data):

    presets = load_presets()

    metadata = input_data["control_metadata"]

    constraints = get_constraints(
        presets,
        metadata["preset_family"],
        metadata["preset_level"]
    )

    prompt = build_prompt(input_data, constraints)

    raw_output = generate_story(prompt)

    final_output = parse_output(raw_output, input_data["image_id"])

    return final_output


if __name__ == "__main__":
    input_data = {
        "image_id": "img_001",
        "caption_data": {
            "caption_text": "A dog playing with a ball in a park",
            "tokens": ["dog", "playing", "ball", "park"]
        },
        "control_metadata": {
            "preset_family": "Neutral_Descriptive",
            "preset_level": 0,
            "trigger_reason": "initial"
        }
    }

    output = language_layer_pipeline(input_data)
    print(output)