import os
from datetime import datetime
from typing import List, Dict


class IssueGenerator:

    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')

    def generate_issue(self, articles: List[Dict], source_stats: Dict) -> str:
        content = self._generate_header()
        content += self._generate_articles_section(articles)
        content += self._generate_stats_section(source_stats)

        return content

    def _generate_header(self) -> str:
        return f"""# 📖 每日深度阅读 - {self.today}

> 每天只推荐 3-5 篇高质量内容，每篇都值得认真读完

---

"""

    def _generate_articles_section(self, articles: List[Dict]) -> str:
        if not articles:
            return "## ❌ 今日无推荐\n\n没有找到符合质量标准的文章。\n"

        content = ""

        for idx, article in enumerate(articles, 1):
            content += self._generate_single_article(article, idx, len(articles))

        return content

    def _generate_single_article(self, article: Dict, idx: int, total: int) -> str:
        category_emoji = {
            'Research': '🔬',
            'Tools': '🛠️',
            'News': '📰',
            'Tutorial': '📚',
            'Opinion': '💭',
            'Discussion': '💬'
        }

        emoji = category_emoji.get(article.get('category', 'News'), '📰')

        title = article.get('title', 'N/A')
        url = article.get('link', article.get('url', 'N/A'))
        score = article.get('score', 0)
        summary = article.get('summary', 'N/A')
        category = article.get('category', 'News')
        source = article.get('source', 'N/A')

        if source == 'github':
            stars = article.get('stars', 0)
            language = article.get('language', 'N/A')
            meta_info = f"**⭐ Stars:** {stars} | **🔤 Language:** {language}\n"
        elif source == 'arxiv':
            authors = ", ".join(article.get('authors', [])[:3])
            meta_info = f"**👥 Authors:** {authors}\n"
        elif source == 'twitter':
            author = f"@{article.get('author', 'N/A')}"
            meta_info = f"**👤 Author:** {author}\n"
        else:
            meta_info = ""

        stars_str = "⭐" * min(5, round(score / 2))

        section = f"""## {emoji} {idx}/{total} {self._get_section_title(article)}

### [{title}]({url})

{meta_info}**📊 AI 评分:** {stars_str} ({score:.1f}/10)  
**🏷️ 类型:** {category}

**AI 摘要:**
{summary}

---

"""

        return section

    def _get_section_title(self, article: Dict) -> str:
        source = article.get('source', '')
        category = article.get('category', '')

        titles = {
            'github': '开源精选',
            'arxiv': '研究论文',
            'twitter': '深度推文',
            'blog': '技术博客',
            'hackernews': '社区讨论'
        }

        return titles.get(source, '今日推荐')

    def _generate_stats_section(self, source_stats: Dict) -> str:
        content = "\n## 📊 今日数据\n\n"
        content += "| 数据源 | 获取数量 | AI 过滤后 | 最终推荐 |\n"
        content += "|--------|---------|-----------|----------|\n"

        for source, stats in source_stats.items():
            content += f"| {source.title()} | {stats['fetched']} | {stats['filtered']} | {stats['selected']} |\n"

        content += "\n**筛选标准:**\n"
        content += "- AI 评分 ≥ 8.0/10\n"
        content += "- 技术深度 ≥ 7.0/10\n"
        content += "- 时效性 ≤ 3 天（论文除外）\n"
        content += "- 阅读时间 ≤ 30 分钟\n"

        content += "\n---\n\n"
        content += "**📢 反馈:** 想调整筛选标准或添加新数据源，请在下方评论！\n\n"
        content += f"🤖 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        return content
