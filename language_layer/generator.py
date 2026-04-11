import ollama

def generate_story(prompt):
    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0
        }
    )

    return response["message"]["content"]