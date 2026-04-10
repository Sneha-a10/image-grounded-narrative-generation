class ConstraintChecker:

    def check(self, story_text, expected_entities, actual_entities, constraints):

        violations = []

        # HARD RULE: NO_NEW_ENTITIES
        if "NO_NEW_ENTITIES" in constraints:
            extra = set(actual_entities) - set(expected_entities)
            if extra:
                violations.append("NO_NEW_ENTITIES")

        return {
            "violation": len(violations) > 0,
            "violations": violations
        }