import textwrap
import openai

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)


def GPT_Template(prompt):
    openai.api_key = config.get("OpenAI", "api_key")

    userPrompt = textwrap.dedent(
        f"""
        {prompt}
    """
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "使用繁體中文回答"},
            {"role": "user", "content": userPrompt},
        ],
    )

    return response.choices[0].message["content"]
