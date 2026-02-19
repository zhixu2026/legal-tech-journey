import requests
import json

API_KEY = "sk-erhaevbgwhcrnvsoqslvojfhjacdnlnkidskxifanozgxivn"  
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [
        {"role": "user", "content": "请用一句话概括《中华人民共和国个人信息保护法》的核心目的"}
    ],
    "temperature": 0.7
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    print("AI回答：")
    print(result['choices'][0]['message']['content'])
except Exception as e:
    print(f"错误：{e}")