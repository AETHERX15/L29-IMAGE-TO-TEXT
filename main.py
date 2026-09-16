from config import HF_API_KEY
import requests, base64, re
from PIL import Image
from colorama import init,Fore, Style
init(autoreset=True)
URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
"Authorization": f"Bearer {HF_API_KEY}",
"Content-Type": "application/json"
}

VISION_MODELS = [
"moonshotai/Kimi-K2.6:novita",
"meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
"meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova"
]

TEXT_MODELS = [
"Qwen/Qwen2.5-7B-Instruct:together",
"Qwen/Qwen2.5-14B-Instruct:together",
"Qwen/Qwen2.5-32B-Instruct:together",
"mistralai/Mistral-7B-Instruct-v0.3:together",
"mistralai/Mixtral-8x7B-Instruct-v0.1:together"
]

def image_data(path):
    with open(path,"rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

def ask_hf(payload):
    try:
        response=requests.post(url=URL,headers=HEADERS,json=payload)
        if response.status_code !=200:
            return None
        return response.json()
    except Exception as e:
        return str (e)

def get_text(data):
    return data["choices"][0]["message"]["content"].strip()

def ran_model(models,messages,tokens=160,temp=0.3):
    error=None
    for model in models:
        data,error=ask_hf({
            "model":model,
            "messages":messages,
            "max_tokens":tokens,
            "temperature":temp
        })
        if data:
            text=get_text(data)
            if text:
                return text,None
    return None,error or"All Models Failed"

def words(text):
 return re.findall(r"\S+", text.strip())

def exact_words(text, n):
 return " ".join(words(text)[:n])

def end_sentence(text):
 text = text.strip()
 return text if text.endswith((".", "!", "?")) else text + "."