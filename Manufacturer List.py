import time
import requests
import json
import re

def load_prompt_from_file(section):
    with open("prompts.txt", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = rf"\[{section}\]\n(.*?)(?=\n\[|$)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        raise ValueError(f"Prompt section [{section}] not found in prompts.txt")

def query_ollama(prompt, model="deepseek-r1:7b"):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        full_reply = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                content = data.get("message", {}).get("content", "")
                full_reply += content

        return full_reply.strip()

    except Exception as e:
        print("Error talking to Ollama:", e)
        return "Failed."

def get_all_manufacturers_and_models(equipmentType):
    prompt_template = load_prompt_from_file("get_all_manufacturers_and_models")
    prompt = prompt_template.format(equipmentType=equipmentType)
    response = query_ollama(prompt)

    print("Manufacturers and Models:\n", response)

    try:
        # Extract JSON using regex (finds the first JSON-like block)
        json_match = re.search(r"\{[\s\S]+\}", response)
        if not json_match:
            raise ValueError("No valid JSON object found in response.")

        json_text = json_match.group(0)

        # Try loading JSON
        data = json.loads(json_text)

        # Save to file
        with open(f"{equipmentType}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("✅ JSON data saved to equipment_models.json")

    except Exception as e:
        print("❌ Failed to parse or save JSON:", e)


def search_main(manufacturer):
    prompt_template = load_prompt_from_file("search_main")
    prompt = prompt_template.format(manufacturer=manufacturer)
    response = query_ollama(prompt)
    print("Response:\n", response)

def get_charger_specs(manufacturer, equipmentType):
    prompt_template = load_prompt_from_file("get_charger_specs")
    prompt = prompt_template.format(manufacturer=manufacturer, equipmentType=equipmentType)
    response = query_ollama(prompt)
    print(f"{manufacturer} Charger Specs:\n", response)

# Run test
starttime = time.perf_counter()
get_all_manufacturers_and_models("Transformers")
