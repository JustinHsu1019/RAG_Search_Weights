import openai
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

openai.api_key = config.get("OpenAI", "api_key")

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
你好
"""

    system_prompt = """
你是一個女僕，要照著日式女僕的用語
用繁體中文輸出
"""

    output_text = call_gpt(input_text, system_prompt)

    print(output_text)
