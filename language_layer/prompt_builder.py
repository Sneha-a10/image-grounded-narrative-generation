def build_prompt(input_data):
    caption = input_data["caption"]
    signals = input_data["signals"]
    constraints = input_data["constraints"]

    negative_rules = "\n".join([f"- {rule}" for rule in constraints["negative_rules"]])

    prompt = f"""
  You are a controlled story generation system.

Caption:
"{caption}"

Signals:
{signals}

Constraints:
- Max Length: {constraints['max_length']} words
- Tone: {constraints['tone']}
- Perspective: {constraints['perspective']}
- Emotion Constraint: {constraints['allowed_emotion_inference']}

STRICT RULES:
{negative_rules}

Task:
Generate a short story using ONLY the provided signals.

You MUST follow:
- Use only the given entities
- Use only the given environment
- Do not introduce new elements
- Keep it simple and controlled

Return ONLY valid JSON:
{{
  "story_text": "",
  "mentioned_entities": [],
  "mentioned_environment": [],
  "inferred_emotion": ""
}}
"""
    return prompt