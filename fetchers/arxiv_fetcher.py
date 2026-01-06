import requests
import feedparser
from typing import List, Dict
from datetime import datetime, timedelta


class ArxivFetcher:

    def __init__(self, config: Dict):
        self.categories = config.get('categories', [])
        self.days = config.get('days', 3)

    def fetch_papers(self) -> List[Dict]:
        all_papers = []

        for category in self.categories:
            papers = self._fetch_category(category)
            all_papers.extend(papers)

        return self._deduplicate(all_papers)

    def _fetch_category(self, category: str) -> List[Dict]:
        url = f"http://export.arxiv.org/rss/{category}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            feed = feedparser.parse(response.content)
            papers = []

            date_limit = datetime.now() - timedelta(days=self.days)

            for entry in feed.entries:
                published = datetime(*entry.published_parsed[:6])

                if published < date_limit:
                    continue

                paper = {
                    'id': entry.id,
                    'title': entry.title,
                    'authors': [author.name for author in entry.get('authors', [])],
                    'summary': entry.summary,
                    'link': entry.link,
                    'published': entry.published,
                    'source': 'arxiv',
                    'category': category
                }
                papers.append(paper)

            return papers

        except requests.exceptions.RequestException as e:
            print(f"Error fetching arXiv papers for {category}: {e}")
            return []

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        seen = set()
        unique_items = []

        for item in items:
            key = item['id']
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items
