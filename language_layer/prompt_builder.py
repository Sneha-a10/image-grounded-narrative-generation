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

Attributes:
{signals.get("attributes", [])}

CONSTRAINTS:
- Max Length: {constraints['max_length']} words
- Tone: {constraints['tone']}
- Perspective: {constraints['perspective']}

STRICT RULES:
{negative_rules}
STRICT OUTPUT REQUIREMENTS:
- The story MUST be 2 to 3 full sentences
- Total length MUST be at least 25–40 words
- MUST clearly describe the scene, actions, and setting
- MUST include the main subject and at least one object
- MUST include some natural detail (lighting, position, interaction, etc.)
- MUST sound like a natural human description, not a label

- DO NOT produce short phrases like:
  "X in place", "object present", "entity exists"

- Even if signals are weak, intelligently expand into a realistic scene

FAILURE TO FOLLOW THESE RULES IS NOT ALLOWED

GOOD EXAMPLE STORY:
"A white cat with bright green eyes cautiously peeks through a dense bush, partially hidden among the leaves. 
It watches its surroundings attentively, as if observing something beyond the frame in a quiet outdoor setting."

Return ONLY valid JSON:

{{
  "story_text": "",
  "mentioned_entities": [],
  "mentioned_environment": [],
  "inferred_emotion": ""
}}
"""
    return prompt