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

# def query_ollama(prompt, model="phi3"):
#     url = "http://localhost:11434/api/chat"
#     payload = {
#         "model": model,
#         "messages": [{"role": "user", "content": prompt}],
#         "stream": True
#     }
#     try:
#         response = requests.post(url, json=payload, stream=True)
#         response.raise_for_status()
#         full_reply = ""
#         for line in response.iter_lines():
#             if line:
#                 data = json.loads(line.decode('utf-8'))
#                 content = data.get("message", {}).get("content", "")
#                 full_reply += content
#         return full_reply.strip()
#     except Exception as e:
#         print("Error talking to Ollama:", e)
#         return "Failed."

from google import genai


def genaiGeneratedModels(query):
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key='AIzaSyD0x_Tcqn06ACnFnCBkmc1jvgZxaILN75Y')

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=query
    )
    return (response.text)

def get_all_manufacturers_and_models(equipmentType):
    try:
        prompt_template = load_prompt_from_file("get_all_manufacturers_and_models")
        print("Raw prompt template:", repr(prompt_template))  # Debug
        # Replace {equipmentType} in the prompt
        prompt = prompt_template.replace("{equipmentType}", equipmentType)
        print("Formatted prompt:", prompt)  # Debug

        # response = query_ollama(prompt)
        response = genaiGeneratedModels(prompt)

        print(f"Manufacturers and Models for {equipmentType}:\n", response)

        json_match = re.search(r"\{[\s\S]*\}", response)
        if not json_match:
            raise ValueError("No valid JSON object found in response.")

        json_text = json_match.group(0)
        data = json.loads(json_text)

        output_file = f"{equipmentType}_models.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"✅ JSON data saved to {output_file}")
        return data

    except KeyError as e:
        print(f"❌ KeyError in formatting prompt: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to parse or save JSON: {e}")
        return None


def get_all_manufacturers(equipmentType):
    try:
        prompt_template = load_prompt_from_file("get_all_manufacturers")
        print("Raw prompt template:", repr(prompt_template))  # Debug
        # Replace {equipmentType} in the prompt
        prompt = prompt_template.replace("{equipmentType}", equipmentType)
        print("Formatted prompt:", prompt)  # Debug

        # response = query_ollama(prompt)
        response = genaiGeneratedModels(prompt)

        print(f"Manufacturers and Models for {equipmentType}:\n", response)

        json_match = re.search(r"\{[\s\S]*\}", response)
        if not json_match:
            raise ValueError("No valid JSON object found in response.")

        json_text = json_match.group(0)
        data = json.loads(json_text)

        output_file = f"{equipmentType}_manufacturers.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"✅ JSON data saved to {output_file}")
        return data

    except KeyError as e:
        print(f"❌ KeyError in formatting prompt: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to parse or save JSON: {e}")
        return None

def get_models_by_manufacturer(equipmentType, manufacturer):
    try:
        prompt_template = load_prompt_from_file("get_models_by_manufacturer")
        print("Raw prompt template:", repr(prompt_template))  # Debug
        # Replace {equipmentType} in the prompt
        prompt = prompt_template.replace("{equipmentType}", equipmentType)
        prompt = prompt.replace("{manufacturer}", manufacturer)
        print("Formatted prompt:", prompt)  # Debug

        # response = query_ollama(prompt)
        response = genaiGeneratedModels(prompt)

        print(f"Manufacturers and Models for {equipmentType}:\n", response)

        json_match = re.search(r"\{[\s\S]*\}", response)
        if not json_match:
            raise ValueError("No valid JSON object found in response.")

        json_text = json_match.group(0)
        data = json.loads(json_text)

        output_file = f"{equipmentType}_{manufacturer}_models.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"✅ JSON data saved to {output_file}")
        return data

    except KeyError as e:
        print(f"❌ KeyError in formatting prompt: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to parse or save JSON: {e}")
        return None


if __name__ == "__main__":
    start_time = time.perf_counter()
    get_models_by_manufacturer("Electrical Panel", "Schneider Electric")
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
