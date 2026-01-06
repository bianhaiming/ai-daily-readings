from typing import List, Dict
from llm.nvidia_client import NvidiaClient


class ArticleFilter:

    def __init__(self, config: Dict, llm_client: NvidiaClient):
        self.minimum_score = config.get('minimum_score', 8.0)
        self.llm_client = llm_client

    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        filtered_articles = []

        for article in articles:
            score_result = self.llm_client.score_article(article)

            if score_result.get('recommended', False):
                article['score'] = score_result.get('score', 0)
                article['score_breakdown'] = score_result.get('breakdown', {})
                article['score_reason'] = score_result.get('reason', '')
                filtered_articles.append(article)

        return filtered_articles

    def rank_articles(self, articles: List[Dict]) -> List[Dict]:
        return sorted(articles, key=lambda x: x.get('score', 0), reverse=True)

    def select_top_articles(self, articles: List[Dict], daily_limit: int) -> List[Dict]:
        ranked = self.rank_articles(articles)
        return ranked[:daily_limit]

    def add_summaries(self, articles: List[Dict]) -> List[Dict]:
        for article in articles:
            article['summary'] = self.llm_client.generate_summary(article)

        return articles

    def classify_articles(self, articles: List[Dict]) -> List[Dict]:
        for article in articles:
            article['category'] = self.llm_client.classify_article(article)

        return articles
