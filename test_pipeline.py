from main_pipeline import Pipeline

# Minimal valid input
data = {
    "image_id": "img_001",
    "caption_data": {
        "caption_text": "A dog playing in a park"
    },
    "visual_features": {
        "embedding_vector": [0.1, 0.2, 0.3]
    },
    "generation_output": {
        "story_text": "dog playing in park",
        "sentences": ["dog playing in park"],
        "word_count": 4
    },
    "signal_extraction": {
        "semantic_signals": {
            "subjects": ["dog"],
            "objects": ["ball"],
            "environment": ["park"],
            "actions": ["playing"],
            "attributes": ["happy"]
        }
    },
    "constraints": {
        "negative_rules": ["NO_NEW_ENTITIES"]
    }
}

pipeline = Pipeline("Neutral_Descriptive")

result = pipeline.run(data)

print(result)