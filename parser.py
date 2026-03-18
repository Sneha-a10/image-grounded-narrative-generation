import json

def parse_output(raw_output, image_id):
    try:
        data = json.loads(raw_output)
        data["image_id"] = image_id
        return data
    except:
        return {
            "image_id": image_id,
            "error": "Invalid JSON output"
        }