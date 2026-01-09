import os
import requests

API_KEY = "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"
URL = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("🧪 测试 NVIDIA API - GLM-4.7 模型")
print("=" * 50)

# 测试 1: 简单对话
print("\n测试 1: 简单对话")
print("-" * 50)

data = {
    "model": "z-ai/glm4.7",
    "messages": [{"role": "user", "content": "你好，请简单介绍一下你自己"}],
    "temperature": 0.7,
    "max_tokens": 500
}

try:
    response = requests.post(URL, json=data, headers=headers, timeout=60)
    response.raise_for_status()
    result = response.json()
    
    if 'choices' in result and len(result['choices']) > 0:
        content = result['choices'][0]['message']['content']
        print(f"✅ 响应成功！")
        print(f"\n{content}")
    else:
        print(f"❌ 响应格式异常: {result}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ 请求失败: {e}")

# 测试 2: JSON 格式输出
print("\n\n测试 2: JSON 格式输出")
print("-" * 50)

data2 = {
    "model": "z-ai/glm4.7",
    "messages": [{"role": "user", "content": "请返回 JSON 格式：{\"test\": \"success\"}"}],
    "temperature": 0.3,
    "max_tokens": 100
}

try:
    response = requests.post(URL, json=data2, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()
    
    if 'choices' in result and len(result['choices']) > 0:
        content = result['choices'][0]['message']['content']
        print(f"✅ JSON 输出测试成功！")
        print(f"\n响应: {content}")
    else:
        print(f"❌ 响应格式异常: {result}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ JSON 测试失败: {e}")

print("\n" + "=" * 50)
print("🎉 测试完成！")
