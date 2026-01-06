import os
import requests
from typing import List, Dict
from datetime import datetime, timedelta


class GitHubFetcher:

    def __init__(self, config: Dict):
        self.topics = config.get('topics', [])
        self.languages = config.get('trending_languages', [])
        self.min_stars = config.get('min_stars', 100)
        self.days = config.get('days', 7)
        self.token = os.environ.get('GITHUB_TOKEN')

        if not self.token:
            print("⚠️  GITHUB_TOKEN 未设置，使用匿名访问（速率限制较低）")

    def fetch_trending(self) -> List[Dict]:
        print(f"  🔍 搜索语言: {self.languages}")
        print(f"  🔍 主题: {self.topics}")
        print(f"  🔍 最小 stars: {self.min_stars}")
        print(f"  🔍 最近 {self.days} 天")

        projects = []

        for language in self.languages:
            query = self._build_trending_query(language)
            print(f"  🔍 查询: {query}")
            results = self._search_repositories(query)
            projects.extend(results)

        return self._deduplicate(projects)

    def _build_trending_query(self, language: str) -> str:
        date_limit = (datetime.now() - timedelta(days=self.days)).strftime('%Y-%m-%d')

        query_parts = [
            f"stars:>{self.min_stars}",
            f"pushed:>{date_limit}",
            f"language:{language}"
        ]

        if self.topics:
            topic_filter = " OR ".join([f"topic:{topic}" for topic in self.topics])
            query_parts.append(f"({topic_filter})")

        return " ".join(query_parts)

    def _search_repositories(self, query: str) -> List[Dict]:
        url = "https://api.github.com/search/repositories"

        headers = {}
        if self.token:
            headers['Authorization'] = f"token {self.token}"

        params = {
            'q': query,
            'sort': 'updated',
            'order': 'desc',
            'per_page': 10
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            total_count = data.get('total_count', 0)
            items = data.get('items', [])

            print(f"  📊 总共 {total_count} 个仓库，获取前 {len(items)} 个")

            return [self._format_repo(item) for item in items]

        except requests.exceptions.RequestException as e:
            print(f"  ❌ 搜索 GitHub 仓库失败: {e}")
            return []

    def _format_repo(self, repo: Dict) -> Dict:
        return {
            'id': repo['id'],
            'title': repo['name'],
            'full_name': repo['full_name'],
            'description': repo.get('description', ''),
            'url': repo['html_url'],
            'stars': repo['stargazers_count'],
            'language': repo.get('language', ''),
            'updated_at': repo['updated_at'],
            'created_at': repo['created_at'],
            'topics': repo.get('topics', []),
            'readme': self._get_readme_url(repo['full_name']),
            'source': 'github',
            'published': repo['created_at']
        }

    def _get_readme_url(self, full_name: str) -> str:
        return f"https://api.github.com/repos/{full_name}/readme"

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        seen = set()
        unique_items = []

        for item in items:
            key = item['id']
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items
