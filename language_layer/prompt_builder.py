def build_prompt(input_data):
    caption = input_data["caption"]
    signals = input_data["signals"]
    constraints = input_data["constraints"]

    negative_rules = "\n".join([f"- {rule}" for rule in constraints["negative_rules"]])

    prompt = f"""
You are a STRICT controlled story generator.

You MUST follow the given signals EXACTLY.

INPUT:

Caption:
"{caption}"

Subject:
{signals["subject"]}

Objects:
{signals["objects"]}

Environment:
{signals["environment"]}

Action:
{signals["action_state"]}

Emotion:
{signals["emotion_hint"]}

CONSTRAINTS:
- Max Length: {constraints['max_length']} words
- Tone: {constraints['tone']}
- Perspective: {constraints['perspective']}

STRICT RULES:
{negative_rules}

HARD REQUIREMENTS:
- DO NOT introduce new entities
- ONLY use listed subject and objects
- ONLY use listed environment
- KEEP story simple and direct
- Emotion must match given emotion

Return ONLY valid JSON:

{{
  "story_text": "",
  "mentioned_entities": [],
  "mentioned_environment": [],
  "inferred_emotion": ""
}}
"""
    return prompt