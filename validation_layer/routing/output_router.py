class OutputRouter:

    def route(self, decision, image_id, story_payload, failure_type, retry_count):

        if decision == "ACCEPT":
            return {
                "route": "TTS",
                "status": "success",
                "data": {
                    "image_id": image_id,
                    "story_payload": story_payload
                }
            }

        elif decision == "REJECT":
            return {
                "route": "REGENERATION",
                "status": "retry",
                "data": {
                    "image_id": image_id,
                    "story_payload": story_payload,  # useful for debugging
                    "retry_count": retry_count + 1,
                    "failure_type": failure_type
                }
            }

        # safety fallback
        return {
            "route": "ERROR",
            "status": "invalid_decision",
            "data": {
                "decision": decision
            }
        }