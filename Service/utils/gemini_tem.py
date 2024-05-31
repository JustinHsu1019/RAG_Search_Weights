import requests, json, sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.config_log as config_log
config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

def Gemini_Template(prompt, max_retries=5):
    api_key = config.get("Gemini", 'api_key')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}'
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    retry_count = 0
    while retry_count < max_retries:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Text not found')
        else:
            wait_time = 2 ** retry_count
            logger.warning(f"Request failed with status code {response.status_code}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retry_count += 1

    logger.error(f"Request failed after {max_retries} retries.")
    return "Failed to get response after multiple retries."

if __name__ == "__main__":
    prompt = f"""告訴我 CTF 逆向分析的 3 個訣竅"""
    print(Gemini_Template(prompt))
