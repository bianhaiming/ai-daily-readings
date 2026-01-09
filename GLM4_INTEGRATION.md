# 🚀 GLM-4.7 模型集成指南

---

## ✅ 已完成的修改

### 1. 更新了 NVIDIA 客户端
- ✅ 支持 GLM-4.7 模型（`z-ai/glm4.7`）
- ✅ 自动识别 GLM 模型并处理特殊响应格式
- ✅ 从 `reasoning_content` 提取最终答案
- ✅ 添加 `system_prompt` 支持

### 2. 更新了配置文件
- ✅ 添加 `nvidia_model` 配置项
- ✅ 默认使用 `z-ai/glm4.7` 模型

---

## 🔧 配置说明

### 当前配置

**文件：** `config/sources.json`

```json
{
  "daily_limit": 5,
  "minimum_score": 8.0,
  "llm_provider": "nvidia",
  "nvidia_model": "z-ai/glm4.7",
  "sources": {
    ...
  }
}
```

### 可用的 NVIDIA 模型

| 模型 | 说明 | 使用方式 |
|-----|------|---------|
| `z-ai/glm4.7` | GLM-4.7（默认） | `"nvidia_model": "z-ai/glm4.7"` |
| `meta/llama-3.1-70b-instruct` | Llama 3.1 70B | `"nvidia_model": "meta/llama-3.1-70b-instruct"` |
| `meta/llama-3.1-8b-instruct` | Llama 3.1 8B | `"nvidia_model": "meta/llama-3.1-8b-instruct"` |
| `mistralai/mistral-large` | Mistral Large | `"nvidia_model": "mistralai/mistral-large"` |

### 切换模型

**编辑 `config/sources.json`:**

```json
{
  "nvidia_model": "meta/llama-3.1-70b-instruct"
}
```

---

## 🎯 GLM-4.7 模型特点

### 优势
- ✅ **思维链能力**：提供完整的推理过程
- ✅ **中文支持好**：理解中文指令和生成中文内容
- ✅ **JSON 输出稳定**：可以生成格式化的 JSON
- ✅ **免费额度充足**：NVIDIA 免费额度支持大量调用

### 特殊行为
GLM-4.7 使用 `reasoning_content` 字段存储思考过程：

```json
{
  "choices": [
    {
      "message": {
        "content": null,
        "reasoning_content": "完整的推理过程...",
        "tool_calls": null
      }
    }
  ]
}
```

**代码自动处理：**
- 如果 `content` 不为 null，使用 `content`
- 如果 `content` 为 null，从 `reasoning_content` 中提取最终答案
- 支持多种提取方式：JSON 块、最后一行等

---

## 📋 使用示例

### 示例 1：文章评分

```python
from llm.nvidia_client import NvidiaClient

client = NvidiaClient(model="z-ai/glm4.7")

article = {
    'title': 'Python 异步编程',
    'summary': '本文介绍 async/await 机制...',
    'source': 'medium'
}

score_result = client.score_article(article)
# 返回: {"score": 8.5, "recommended": true, "reason": "..."}
```

### 示例 2：生成摘要

```python
from llm.nvidia_client import NvidiaClient

client = NvidiaClient(model="z-ai/glm4.7")

article = {
    'title': 'AI 领域最新技术',
    'content': '长篇文章内容...'
}

summary = client.generate_summary(article, max_length=150)
# 返回: "本文介绍了 AI 领域的最新技术进展..."
```

### 示例 3：直接对话

```python
from llm.nvidia_client import NvidiaClient

client = NvidiaClient(model="z-ai/glm4.7")

response = client.chat("你好，请介绍一下你自己")
print(response)
# 返回完整的中文回答
```

---

## 🧪 测试集成

### 本地测试

```bash
cd /Users/bianhaiming/ai-daily-readings

# 运行测试脚本
python3 -c "
from llm.nvidia_client import NvidiaClient

client = NvidiaClient()
print(f'当前模型: {client.model}')
print(f'是 GLM 模型: {client.is_glm_model}')

# 测试评分
article = {
    'title': '测试文章',
    'summary': '这是一个测试',
    'source': 'test'
}

result = client.score_article(article)
print(f'评分结果: {result}')
"
```

### 完整流程测试

```bash
# 安装依赖
python3 -m pip install -r requirements.txt

# 运行主脚本
python3 main.py
```

---

## ⚙️ 高级配置

### 添加 system_prompt

```python
client = NvidiaClient(model="z-ai/glm4.7")

response = client.chat(
    prompt="帮我分析这段代码",
    system_prompt="你是一个代码分析专家，专注于性能优化..."
)
```

### 调整参数

```python
# 降低 temperature 以获得更确定的输出
result = client.score_article(article, temperature=0.1)

# 增加 max_tokens 以获得更长的响应
summary = client.generate_summary(article, max_tokens=500)
```

---

## 🐛 故障排查

### 问题 1：JSON 解析失败

**现象：**
```
Failed to parse JSON response: ...
```

**解决方法：**
1. GLM-4.7 可能返回多余的文字，已自动处理
2. 检查 `reasoning_content` 中是否包含完整的 JSON
3. 尝试降低 `temperature` 参数

### 问题 2：响应为空

**现象：**
```
响应为空
```

**解决方法：**
1. 检查 API Key 是否正确
2. 验证网络连接
3. 查看错误日志

### 问题 3：评分不准确

**解决方法：**
1. 调整 `minimum_score` 阈值
2. 修改评分 prompt 的权重
3. 增加示例提高理解

---

## 📊 与 Llama 3.1 对比

| 特性 | GLM-4.7 | Llama 3.1 |
|-----|---------|----------|
| **思维链** | ✅ 详细推理过程 | ⚠️ 简单推理 |
| **中文支持** | ✅ 优秀 | ✅ 良好 |
| **JSON 输出** | ✅ 稳定 | ✅ 稳定 |
| **速度** | ⚠️ 稍慢（需要推理） | ✅ 较快 |
| **准确性** | ✅ 更准确 | ✅ 准确 |

---

## 🎓 提示词优化建议

### 评分提示词

**当前特点：**
- 多维度评分（技术深度、实用性等）
- 加权计算
- JSON 格式强制输出

**优化建议：**
```python
# 添加示例
prompt = """
示例：
标题: "Vue3 源码分析"
摘要: "深入理解 Vue3 的响应式系统..."

评分结果：
{"score": 9.0, "recommended": true, "reason": "技术深度高，实用性强"}

现在评估：
...
"""
```

### 摘要提示词

**优化建议：**
```python
# 添加风格要求
prompt = """
生成摘要时，遵循以下风格：
1. 开头直接切入重点
2. 突出技术要点
3. 避免冗余描述
4. 控制在指定字数内

文章标题: {title}
文章内容: {content}
"""
```

---

## 🚀 下一步

### 1. 测试完整流程
```bash
cd /Users/bianhaiming/ai-daily-readings
python3 main.py
```

### 2. 推送到 GitHub
```bash
git add .
git commit -m "Integrate GLM-4.7 model"
git push origin main
```

### 3. 运行 GitHub Actions
- 访问 Actions 页面
- 手动触发 workflow
- 查看生成的 Issue

---

## 📞 获取帮助

**遇到问题？**

1. 查看 NVIDIA API 文档：https://build.nvidia.com
2. 查看 GLM-4 文档：https://z.ai
3. 创建 GitHub Issue

---

**🎉 GLM-4.7 已成功集成！享受更强大的 AI 推荐体验吧！**
