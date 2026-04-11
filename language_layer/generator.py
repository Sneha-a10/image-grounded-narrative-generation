import ollama

# def generate_story(prompt):
#     response = ollama.chat(
#         model="mistral",
#         messages=[{"role": "user", "content": prompt}],
#         options={
#             "temperature": 0
#         },
#         format="json"
#     )
#     return response["message"]["content"]

def generate_story(prompt):
    return """
    {
        "story_text": "A character stands next to a fox.",
        "mentioned_entities": ["character", "fox"],
        "mentioned_environment": [],
        "inferred_emotion": "neutral"
    }
    """