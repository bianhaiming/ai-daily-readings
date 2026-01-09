import requests
from typing import List, Dict
from datetime import datetime


class HackerNewsFetcher:

    def __init__(self, config: Dict):
        self.min_score = config.get('min_score', 100)
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    def fetch_stories(self) -> List[Dict]:
        return self._fetch_best_stories()

    def _fetch_best_stories(self) -> List[Dict]:
        url = f"{self.base_url}/beststories.json"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            story_ids = response.json()
            stories = []
            ai_keywords = ['ai', 'artificial', 'machine learning', 'neural', 'deep learning', 'llm', 'gpt', 'model', 'chatgpt']

            # 只获取前 20 个故事
            for story_id in story_ids[:20]:
                story_detail = self._fetch_story_detail(story_id)

                if story_detail and story_detail.get('score', 0) >= self.min_score:
                    title = story_detail.get('title', '').lower()

                    # 检查是否是 AI 相关的
                    if any(keyword in title for keyword in ai_keywords):
                        story = {
                            'id': story_id,
                            'title': story_detail.get('title', 'N/A'),
                            'url': story_detail.get('url') or f"https://news.ycombinator.com/item?id={story_id}",
                            'score': story_detail.get('score', 0),
                            'author': story_detail.get('by', 'N/A'),
                            'published': datetime.fromtimestamp(story_detail.get('time', 0)).isoformat(),
                            'descendants': story_detail.get('descendants', 0),
                            'source': 'hackernews'
                        }
                        stories.append(story)

            return stories

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Hacker News stories: {e}")
            return []

    def _fetch_story_detail(self, story_id: str) -> Dict:
        url = f"{self.base_url}/item/{story_id}.json"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException:
            return {}

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        seen = set()
        unique_items = []

        for item in items:
            key = item['id']
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items
