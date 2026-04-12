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

    if "error" in final_output:
        print(f"⚠️  LANGUAGE LAYER FALLBACK TRIGGERED: {final_output['error']}")
        # ---- DYNAMIC FALLBACK GENERATOR ----

        signals = input_data.get("signals", {})
        constraints = input_data.get("constraints", {})
        negative_rules = constraints.get("negative_rules", [])

        subject = signals.get("subject", "something")
        environment = signals.get("environment", ["place"])
        environment = environment[0] if environment else "place"

        # Infer strictness from number of constraints
        strictness = len(negative_rules)

        # ---- GENERATE BASED ON STRICTNESS ----
        if strictness <= 1:
            story = f"A {subject} is in a {environment}."

        elif strictness == 2:
            story = f"{subject} in {environment}."

        elif strictness == 3:
            story = f"{subject} in {environment}."

        else:
            story = f"{subject} in {environment}."


        return {
            "story_text": story,
            "mentioned_entities": [subject],
            "mentioned_environment": [environment],
            "inferred_emotion": "neutral"
        }

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