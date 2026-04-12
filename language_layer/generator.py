import ollama

def generate_story(prompt):
    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={
            "temperature": 0
        }
    )

    raw_content = response["message"]["content"]
    print("\n🔍 RAW LLM OUTPUT:\n", raw_content)
    return raw_content