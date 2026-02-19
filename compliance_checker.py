import requests
import json

API_KEY = "sk-erhaevbgwhcrnvsoqslvojfhjacdnlnkidskxifanozgxivn" 
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

def check_compliance(data_description, destination_country):
    prompt = f"""
    请判断以下场景的合规风险：
    
    数据类型：{data_description}
    传输目的地：{destination_country}
    
    请参考：
    1. 中国《个人信息保护法》及《生成式人工智能服务管理暂行办法》
    2. 欧盟GDPR
    3. 美国CCPA
    
    请输出：
    1. 风险等级（高/中/低）
    2. 主要风险点
    3. 建议措施
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        # 检查HTTP状态码
        if response.status_code != 200:
            return f"HTTP错误 {response.status_code}: {response.text}"
        
        result = response.json()
        # 检查API返回的JSON是否包含预期字段
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return f"API返回异常: {result}"
    except Exception as e:
        return f"请求异常: {str(e)}"

if __name__ == "__main__":
    test_cases = [
        {"data": "中国用户实名认证信息（姓名+身份证号）", "to": "欧盟"},
        {"data": "匿名化处理的用户行为日志", "to": "美国"},
        {"data": "企业内部员工通讯录", "to": "新加坡"}
    ]
    
    for case in test_cases:
        print(f"\n--- 测试场景 ---")
        print(f"数据：{case['data']}")
        print(f"目的地：{case['to']}")
        print("结果：")
        result = check_compliance(case['data'], case['to'])
        print(result)
        print("-" * 50)