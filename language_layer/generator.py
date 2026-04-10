import ollama

def generate_story(prompt):
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0
        },
        format="json"
    )
    return response["message"]["content"]