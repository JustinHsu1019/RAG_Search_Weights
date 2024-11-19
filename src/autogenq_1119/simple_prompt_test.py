import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def call_gpt(prompt, system_prompt=""):
    """Calls the OpenAI API with the given prompt and returns the response."""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    input_text = """
"""

    system_prompt = """

"""

    output_text = call_gpt(input_text, system_prompt)

    print("\n\nGPT 輸出：\n\n")
    print(output_text)
