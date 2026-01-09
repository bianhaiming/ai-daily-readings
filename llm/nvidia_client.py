import os
import requests
import json
import re
from typing import Dict, Optional


class NvidiaClient:

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.environ.get('NVIDIA_API_KEY')
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is required")

        self.base_url = "https://integrate.api.nvidia.com/v1"

        self.model = model or "meta/llama-3.1-70b-instruct"

        self.is_glm_model = self.model.startswith('z-ai/glm')

    def chat(self, prompt: str, temperature: float = 0.3, max_tokens: int = 1000, 
             system_prompt: Optional[str] = None) -> str:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            result = response.json()

            if self.is_glm_model:
                return self._extract_glm_response(result)
            else:
                return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            print(f"Error calling NVIDIA API: {e}")
            return ""

    def _extract_glm_response(self, result: Dict) -> str:
        """从 GLM-4.7 响应中提取最终答案"""
        if 'choices' not in result or len(result['choices']) == 0:
            return ""

        choice = result['choices'][0]
        message = choice.get('message', {})
        content = message.get('content')
        reasoning = message.get('reasoning_content')

        if content:
            return content

        if reasoning:
            final_answer = self._extract_final_answer(reasoning)
            if final_answer:
                return final_answer

        return reasoning if reasoning else ""

    def _extract_final_answer(self, reasoning: str) -> Optional[str]:
        """从思考过程中提取最终答案"""
        lines = reasoning.strip().split('\n')

        for line in reversed(lines):
            line = line.strip()

            if not line:
                continue

            if line.startswith('```json'):
                return self._extract_json_block(reasoning)
            elif line.startswith('```'):
                continue
            elif line.startswith('{') or line.startswith('"'):
                try:
                    json.loads(line)
                    return line
                except:
                    continue

        return None

    def _extract_json_block(self, reasoning: str) -> Optional[str]:
        """从思考过程中提取 JSON 代码块"""
        json_pattern = r'```json\s*(\{[^}]*\})\s*```'
        matches = re.findall(json_pattern, reasoning, re.DOTALL)

        if matches:
            return matches[-1].strip()

        json_pattern2 = r'(\{[^{}]*\})'
        matches2 = re.findall(json_pattern2, reasoning)

        if matches2:
            return matches2[-1].strip()

        return None

    def score_article(self, article: Dict) -> Dict:
        system_prompt = """你是一个文章评分助手，评估文章质量并返回纯 JSON 格式。
重要：只在最后一行返回 JSON，不要包含任何其他文字或思考过程。"""

        prompt = f"""评估以下文章（返回纯 JSON 格式，不要包含任何其他文字）：

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

        response = self.chat(prompt, temperature=0.1, system_prompt=system_prompt, max_tokens=500)
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

        system_prompt = """你是一个文章分类助手，只返回类别名称。
重要：只返回一个类别名称，不要包含其他文字。"""

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

        category = self.chat(prompt, temperature=0.1, system_prompt=system_prompt, max_tokens=50)
        category = category.strip()
        valid_categories = ['Research', 'Tools', 'News', 'Tutorial', 'Opinion', 'Discussion']

        if category in valid_categories:
            return category
        else:
            return 'News'
