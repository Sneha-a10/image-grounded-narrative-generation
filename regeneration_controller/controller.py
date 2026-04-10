class RegenerationController:

    def __init__(self, preset_family, user_negative_prompts=None, max_level=2):
        self.preset_family = preset_family
        self.retry_count = 0
        self.max_level = max_level
        self.user_negative_prompts = user_negative_prompts or []

    def handle_rejection(self, failure_type):

        self.retry_count += 1

        # HARD STOP CONDITION
        if self.retry_count > self.max_level:
            return {
                "action": "STOP",
                "reason": "MAX_RETRIES_EXCEEDED"
            }

        return {
            "action": "RETRY",
            "constraint_input": {
                "experiment_mode": self.preset_family,
                "retry_count": self.retry_count,
                "failure_type": failure_type
            },
            "user_negative_prompts": self.user_negative_prompts
        }