REQUIRED_SCHEMA = {
    "image_id": str,

    "caption_data": {
        "caption_text": str
    },

    "visual_features": {
        "embedding_vector": list
    },

    "generation_output": {
        "story_text": str,
        "sentences": list,
        "word_count": int
    },

    "signal_extraction": {
        "semantic_signals": {
            "subjects": list,
            "objects": list,
            "environment": list,
            "actions": list,
            "attributes": list
        }
    },

    "constraints": {
        "negative_rules": list
    }
}