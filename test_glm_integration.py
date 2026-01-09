import os
import json
sys.path.insert(0, '/Users/bianhaiming/ai-daily-readings')

from llm.nvidia_client import NvidiaClient

print('🧪 测试 GLM-4.7 集成')
print('=' * 50)

# 创建客户端（从配置文件加载）
with open('/Users/bianhaiming/ai-daily-readings/config/sources.json', 'r') as f:
    config = json.load(f)

model = config.get('nvidia_model', 'z-ai/glm4.7')
print(f'\n✅ 加载模型: {model}')

client = NvidiaClient(model=model)
print(f'✅ 是 GLM 模型: {client.is_glm_model}')

# 测试 1: 简单对话
print('\n测试 1: 简单对话')
print('-' * 50)
response = client.chat('你好，简单介绍一下你自己', temperature=0.7, max_tokens=100)
print(f'响应: {response[:100]}...' if len(response) > 100 else f'响应: {response}')

# 测试 2: JSON 输出
print('\n测试 2: JSON 评分')
print('-' * 50)

article = {
    'title': 'Python 异步编程',
    'summary': '介绍 async/await 机制',
    'source': 'medium',
    'published': '2025-12-15'
}

score_result = client.score_article(article)
print(f'评分结果:')
print(f'  Score: {score_result.get("score", 0)}')
print(f'  Recommended: {score_result.get("recommended", False)}')
print(f'  Reason: {score_result.get("reason", "N/A")}')

# 测试 3: 摘要生成
print('\n测试 3: 摘要生成')
print('-' * 50)

article2 = {
    'title': 'React Hooks 最佳实践',
    'content': 'Hooks 改变了我们编写组件的方式...'
}

summary = client.generate_summary(article2, max_length=80)
print(f'摘要: {summary}')

print('\n' + '=' * 50)
print('🎉 所有测试完成！')
