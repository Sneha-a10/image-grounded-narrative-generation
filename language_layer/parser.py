import json
import re

def parse_output(raw_output, image_id, signals):
    try:
        # Extract JSON block using regex
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)

        if not match:
            raise ValueError("No JSON found")

        json_str = match.group(0)

        data = json.loads(json_str)

        # Validate alignment with signals
        entities = set(data["mentioned_entities"])
        allowed_entities = set([signals["subject"]] + signals["objects"])

        if not entities.issubset(allowed_entities):
            raise ValueError("Invalid entities detected")

        env = set(data["mentioned_environment"])
        allowed_env = set(signals["environment"])

        if not env.issubset(allowed_env):
            raise ValueError("Invalid environment detected")

        required_keys = {
            "story_text",
            "mentioned_entities",
            "mentioned_environment",
            "inferred_emotion"
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError("Invalid schema")

        data["image_id"] = image_id
        return data

    except Exception as e:
        print(f"❌ PARSING ERROR: {str(e)}")
        return {
            "image_id": image_id,
            "error": f"Invalid JSON or schema: {str(e)}"
        }