def build_prompt(input_data, constraints):
    caption = input_data["caption_data"]["caption_text"]
    tokens = input_data["caption_data"]["tokens"]

    negative_rules = "\n".join([f"- {rule}" for rule in constraints["negative_rules"]])

    prompt = f"""
You are a controlled story generation system.

Caption:
"{caption}"

Tokens:
{tokens}

Constraints:
- Max Length: {constraints['max_length']} words
- Tone: {constraints['tone']}
- Perspective: {constraints['perspective']}
- Emotion Constraint: {constraints['allowed_emotion_inference']}

STRICT RULES:
{negative_rules}

Tasks:
1. Generate a short story grounded ONLY in the caption.
2. Extract:
   - subjects
   - objects
   - environment
   - actions
   - attributes
3. Split into sentences
4. Count words

Return ONLY JSON:
{{
  "signal_extraction": {{
    "semantic_signals": {{
      "subjects": [],
      "objects": [],
      "environment": [],
      "actions": [],
      "attributes": []
    }}
  }},
  "generation_output": {{
    "story_text": "",
    "sentences": [],
    "word_count": 0
  }}
}}
"""
    return prompt