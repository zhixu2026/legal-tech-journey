import requests
import json
import re      # 用于清理AI返回的文本
import sys     # 用于读取命令行参数

# ==================== 配置区 ====================
API_KEY ="sk-erhaevbgwhcrnvsoqslvojfhjacdnlnkidskxifanozgxivn"  
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
# ================================================

def check_compliance(data_description, destination_country):
    """
    调用AI判断数据跨境合规风险，要求返回JSON格式
    """
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

**请以JSON格式输出，包含以下字段：**
- **risk_level**: 字符串，风险等级
- **risk_points**: 数组，每个元素是一条风险点描述
- **suggestions**: 数组，每个元素是一条建议措施

注意：只返回JSON，不要包含任何其他文字、代码块标记或解释。
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
        if response.status_code != 200:
            return f"HTTP错误 {response.status_code}: {response.text}"
        
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return f"API返回异常: {result}"
    except Exception as e:
        return f"请求异常: {str(e)}"

if __name__ == "__main__":
    # ---------- 命令行参数处理 ----------
    if len(sys.argv) == 3:
        # 用户提供了两个参数
        data_desc = sys.argv[1]      # 第一个参数：数据类型
        dest = sys.argv[2]            # 第二个参数：目的地
        test_cases = [{"data": data_desc, "to": dest}]
        print(f"使用命令行参数：数据类型='{data_desc}', 目的地='{dest}'")
    else:
        # 未提供参数或参数数量不对，使用默认测试用例
        print("未检测到命令行参数或参数数量不正确，使用默认测试用例。")
        test_cases = [
            {"data": "中国用户实名认证信息（姓名+身份证号）", "to": "欧盟"},
            {"data": "匿名化处理的用户行为日志", "to": "美国"},
            {"data": "企业内部员工通讯录", "to": "新加坡"}
        ]
    
    # ---------- 处理每个测试用例 ----------
    for case in test_cases:
        print(f"\n--- 测试场景 ---")
        print(f"数据：{case['data']}")
        print(f"目的地：{case['to']}")
        
        result_text = check_compliance(case['data'], case['to'])
        
        # ----- 清理AI返回的文本，去掉可能的Markdown代码块标记 -----
        cleaned_text = result_text.strip()
        
        # 如果文本以 ```json 开头，提取其中的JSON部分
        if cleaned_text.startswith('```json'):
            match = re.search(r'```json\s*(\{.*?\})\s*```', cleaned_text, re.DOTALL)
            if match:
                cleaned_text = match.group(1)
            else:
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
        elif cleaned_text.startswith('```'):
            cleaned_text = cleaned_text.replace('```', '').strip()
        
        # 尝试解析JSON
        try:
            data = json.loads(cleaned_text)
            print("风险等级：", data.get('risk_level', '无'))
            print("风险点：")
            for point in data.get('risk_points', []):
                print(f"  - {point}")
            print("建议：")
            for suggestion in data.get('suggestions', []):
                print(f"  - {suggestion}")
        except Exception as e:
            print("AI返回的不是有效JSON，原始内容：", result_text)
            print("清理后的内容：", cleaned_text)
            print("错误信息：", e)
        print("-" * 50)