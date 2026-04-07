class OutputRouter:

    def route(self, decision, image_id, story_payload, failure_type, retry_count):

        if decision == "ACCEPT":
            return {
                "route": "TTS",
                "data": {
                    "image_id": image_id,
                    "story_payload": story_payload
                }
            }

        return {
            "route": "REGENERATION",
            "data": {
                "image_id": image_id,
                "retry_count": retry_count + 1,
                "failure_type": failure_type
            }
        }