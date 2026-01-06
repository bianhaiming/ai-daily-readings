import requests
from typing import List, Dict
from datetime import datetime, timedelta


class HackerNewsFetcher:

    def __init__(self, config: Dict):
        self.tags = config.get('tags', [])
        self.min_score = config.get('min_score', 100)
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    def fetch_stories(self) -> List[Dict]:
        all_stories = []

        for tag in self.tags:
            stories = self._fetch_by_tag(tag)
            all_stories.extend(stories)

        return self._deduplicate(all_stories)

    def _fetch_by_tag(self, tag: str) -> List[Dict]:
        url = f"{self.base_url}/search/restricted"
        params = {
            'tags': tag,
            'restrictSearchableAttributes': ['url', 'title', 'author'],
            'hitsPerPage': 10
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            stories = []

            for hit in data.get('hits', []):
                story_id = hit.get('objectID')
                story_detail = self._fetch_story_detail(story_id)

                if story_detail and story_detail.get('score', 0) >= self.min_score:
                    story = {
                        'id': story_id,
                        'title': story_detail.get('title', 'N/A'),
                        'url': story_detail.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'score': story_detail.get('score', 0),
                        'author': story_detail.get('by', 'N/A'),
                        'published': story_detail.get('time', 'N/A'),
                        'descendants': story_detail.get('descendants', 0),
                        'source': 'hackernews'
                    }
                    stories.append(story)

            return stories

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Hacker News stories for {tag}: {e}")
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
