from .schema import REQUIRED_SCHEMA

class InputValidator:

    def validate(self, data: dict) -> bool:
        try:
            self._validate_schema(REQUIRED_SCHEMA, data)
            self._validate_non_empty(data)
            self._validate_logical_consistency(data)
            return True
        except Exception:
            return False
    
    def _validate_schema(self, schema, data):
        if not isinstance(data, dict):
            raise Exception("Input must be dict")

        for key, expected_type in schema.items():

            if key not in data:
                raise Exception(f"Missing field: {key}")

            if isinstance(expected_type, dict):
                self._validate_schema(expected_type, data[key])
            else:
                if not isinstance(data[key], expected_type):
                    raise Exception(f"Type mismatch at {key}")

    def _validate_non_empty(self, data):

        if not data["generation_output"]["story_text"]:
            raise Exception("Empty story_text")

        if not data["generation_output"]["sentences"]:
            raise Exception("Empty sentences")

        if not data["visual_features"]["embedding_vector"]:
            raise Exception("Empty embedding_vector")

        signals = data["signal_extraction"]["semantic_signals"]

        if not signals:
            raise Exception("Empty semantic signals dictionary")

        if not data["constraints"]["negative_rules"]:
            raise Exception("Empty negative_rules")

    def _validate_logical_consistency(self, data):

        story = data["generation_output"]["story_text"]
        word_count = data["generation_output"]["word_count"]

        if len(story.split()) != word_count:
            raise Exception("Word count mismatch")