import requests
import feedparser
from typing import List, Dict
import time
import re


class TwitterFetcher:

    def __init__(self, config: Dict):
        self.accounts = config['accounts']
        self.instances = config['nitter_instances']
        self.min_length = config.get('min_length', 500)
        self.min_likes = config.get('min_likes', 100)

    def fetch_all(self) -> List[Dict]:
        all_tweets = []

        for account in self.accounts:
            tweets = self._fetch_user_tweets(account)
            filtered = self._filter_tweets(tweets)
            all_tweets.extend(filtered)

            time.sleep(2)

        return self._deduplicate(all_tweets)

    def _fetch_user_tweets(self, username: str) -> List[Dict]:
        tweets = []

        for instance in self.instances:
            try:
                url = f"{instance}/{username}/rss"
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    feed = feedparser.parse(response.content)

                    for entry in feed.entries:
                        tweet = {
                            'id': entry.id,
                            'author': username,
                            'content': entry.description,
                            'link': entry.link,
                            'published': entry.published,
                            'likes': self._extract_likes(entry)
                        }
                        tweets.append(tweet)

                    break

            except Exception as e:
                print(f"Failed to fetch from {instance} for {username}: {e}")
                continue

        return tweets

    def _extract_likes(self, entry) -> int:
        content = entry.get('description', '')
        match = re.search(r'❤️ ([0-9.]+)(K|M)?', content)

        if match:
            num = float(match.group(1))
            unit = match.group(2)

            if unit == 'K':
                return int(num * 1000)
            elif unit == 'M':
                return int(num * 1000000)
            else:
                return int(num)

        return 0

    def _filter_tweets(self, tweets: List[Dict]) -> List[Dict]:
        filtered = []

        for tweet in tweets:
            if len(tweet['content']) < self.min_length:
                continue

            if tweet['likes'] < self.min_likes:
                continue

            filtered.append(tweet)

        return filtered

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        seen = set()
        unique_items = []

        for item in items:
            key = item['id']
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items
