import requests
import feedparser
from typing import List, Dict


class BlogFetcher:

    def __init__(self, config: Dict):
        self.feeds = config.get('feeds', [])

    def fetch_articles(self) -> List[Dict]:
        all_articles = []

        for feed_url in self.feeds:
            articles = self._fetch_feed(feed_url)
            all_articles.extend(articles)

        return self._deduplicate(all_articles)

    def _fetch_feed(self, feed_url: str) -> List[Dict]:
        try:
            response = requests.get(feed_url, timeout=30)
            response.raise_for_status()

            feed = feedparser.parse(response.content)
            articles = []

            for entry in feed.entries:
                article = {
                    'id': entry.get('id', entry.get('link', '')),
                    'title': entry.get('title', 'N/A'),
                    'summary': entry.get('summary', entry.get('description', '')),
                    'link': entry.get('link', 'N/A'),
                    'published': entry.get('published', entry.get('updated', 'N/A')),
                    'author': entry.get('author', 'N/A'),
                    'source': self._extract_source_name(feed_url)
                }
                articles.append(article)

            return articles

        except requests.exceptions.RequestException as e:
            print(f"Error fetching blog feed {feed_url}: {e}")
            return []

    def _extract_source_name(self, feed_url: str) -> str:
        from urllib.parse import urlparse
        return urlparse(feed_url).netloc

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        seen = set()
        unique_items = []

        for item in items:
            key = item['id'] if item['id'] else item['link']
            if key and key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items
