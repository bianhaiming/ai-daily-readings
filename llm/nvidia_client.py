import os
import requests
import json
from typing import Dict, Optional


class NvidiaClient:

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('NVIDIA_API_KEY')
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is required")

        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "meta/llama-3.1-70b-instruct"

    def chat(self, prompt: str, temperature: float = 0.3, max_tokens: int = 1000) -> str:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            print(f"Error calling NVIDIA API: {e}")
            return ""

    def score_article(self, article: Dict) -> Dict:
        prompt = f"""评估以下文章（返回 JSON 格式，不要包含任何其他文字）：

标题: {article.get('title', 'N/A')}
摘要: {article.get('summary', article.get('content', ''))[:500]}
来源: {article.get('source', 'N/A')}
发布时间: {article.get('published', 'N/A')}

评分维度（0-10）：
1. technical_depth: 技术深度
2. utility: 实用性
3. timeliness: 时效性
4. readability: 可读性
5. credibility: 来源可信度
6. engagement: 社区反响

计算总分（加权平均）：
- technical_depth: 25%
- utility: 20%
- timeliness: 15%
- readability: 15%
- credibility: 10%
- engagement: 15%

返回 JSON 格式（纯 JSON，无其他文字）：
{{"score": 0-10, "breakdown": {{"technical_depth": 0-10, "utility": 0-10, "timeliness": 0-10, "readability": 0-10, "credibility": 0-10, "engagement": 0-10}}, "recommended": true/false, "reason": "..."}}
"""

        response = self.chat(prompt, temperature=0.1)
        response = response.strip()

        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1

        if start_idx != -1 and end_idx > start_idx:
            response = response[start_idx:end_idx]

        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response: {response}")
            return {
                "score": 5.0,
                "breakdown": {
                    "technical_depth": 5.0,
                    "utility": 5.0,
                    "timeliness": 5.0,
                    "readability": 5.0,
                    "credibility": 5.0,
                    "engagement": 5.0
                },
                "recommended": False,
                "reason": "Failed to parse AI response"
            }

    def generate_summary(self, article: Dict, max_length: int = 150) -> str:
        title = article.get('title', 'N/A')
        content = article.get('content', article.get('summary', ''))[:2000]

        prompt = f"""为以下文章生成 {max_length} 字的中文摘要：

标题: {title}
内容: {content}

要求：
1. 简洁明了
2. 突出核心观点
3. 适合开发者阅读
4. 严格控制在 {max_length} 字以内
"""

        summary = self.chat(prompt, temperature=0.5, max_tokens=300)

        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."

        return summary

    def classify_article(self, article: Dict) -> str:
        title = article.get('title', '')
        content = article.get('content', article.get('summary', ''))[:500]

        prompt = f"""将以下文章分类（返回唯一的一个类别名称）：

标题: {title}
内容: {content}

可选类别：
- Research: 研究论文
- Tools: 开发工具或库
- News: 行业新闻
- Tutorial: 教程或指南
- Opinion: 观点或评论
- Discussion: 讨论或对话

返回格式：只返回类别名称，例如：Research"""

        category = self.chat(prompt, temperature=0.1, max_tokens=50)
        category = category.strip()
        valid_categories = ['Research', 'Tools', 'News', 'Tutorial', 'Opinion', 'Discussion']

        if category in valid_categories:
            return category
        else:
            return 'News'
