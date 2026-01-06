import os
import json
from datetime import datetime
from fetchers.github_fetcher import GitHubFetcher
from fetchers.twitter_fetcher import TwitterFetcher
from fetchers.arxiv_fetcher import ArxivFetcher
from fetchers.blog_fetcher import BlogFetcher
from fetchers.hackernews_fetcher import HackerNewsFetcher
from llm.nvidia_client import NvidiaClient
from filters.article_filter import ArticleFilter
from generators.issue_generator import IssueGenerator
import requests


def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'sources.json')

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """主函数"""
    print("🚀 开始 AI 每日推荐工具...")

    config = load_config()
    sources_config = config['sources']
    llm_provider = config.get('llm_provider', 'nvidia')

    print(f"📊 LLM Provider: {llm_provider}")

    llm_client = NvidiaClient()
    article_filter = ArticleFilter(config, llm_client)
    issue_generator = IssueGenerator()

    all_articles = []
    source_stats = {}

    print("\n📡 从各数据源获取内容...")

    for source_name, source_config in sources_config.items():
        if not source_config.get('enabled', False):
            continue

        print(f"\n🔍 处理 {source_name}...")

        try:
            if source_name == 'github':
                fetcher = GitHubFetcher(source_config['config'])
                articles = fetcher.fetch_trending()

            elif source_name == 'twitter':
                fetcher = TwitterFetcher(source_config['config'])
                articles = fetcher.fetch_all()

            elif source_name == 'arxiv':
                fetcher = ArxivFetcher(source_config['config'])
                articles = fetcher.fetch_papers()

            elif source_name == 'blogs':
                fetcher = BlogFetcher(source_config)
                articles = fetcher.fetch_articles()

            elif source_name == 'hackernews':
                fetcher = HackerNewsFetcher(source_config['config'])
                articles = fetcher.fetch_stories()

            else:
                articles = []

            source_stats[source_name] = {
                'fetched': len(articles),
                'filtered': 0,
                'selected': 0
            }

            print(f"  ✓ 获取了 {len(articles)} 篇文章")

            if articles:
                filtered = article_filter.filter_articles(articles)
                source_stats[source_name]['filtered'] = len(filtered)

                daily_limit = source_config.get('daily_limit', 1)
                selected = article_filter.select_top_articles(filtered, daily_limit)
                source_stats[source_name]['selected'] = len(selected)

                print(f"  ✓ AI 过滤后: {len(filtered)} 篇")
                print(f"  ✓ 最终推荐: {len(selected)} 篇")

                all_articles.extend(selected)

        except Exception as e:
            print(f"  ❌ 处理 {source_name} 时出错: {e}")
            source_stats[source_name] = {
                'fetched': 0,
                'filtered': 0,
                'selected': 0
            }

    print(f"\n📝 总共获取了 {len(all_articles)} 篇推荐文章")

    if all_articles:
        print("\n🤖 生成摘要和分类...")
        all_articles = article_filter.add_summaries(all_articles)
        all_articles = article_filter.classify_articles(all_articles)

        print("\n📄 生成 GitHub Issue...")
        issue_content = issue_generator.generate_issue(all_articles, source_stats)

        print(issue_content)

        print("\n✅ Issue 内容生成完成！")

        if os.environ.get('GITHUB_TOKEN'):
            print("\n📤 创建 GitHub Issue...")
            create_github_issue(issue_content)
        else:
            print("\n⚠️  GITHUB_TOKEN 未设置，跳过创建 Issue")

    else:
        print("\n❌ 没有符合条件的文章被推荐")


def create_github_issue(content: str):
    """创建 GitHub Issue"""
    repo = os.environ.get('GITHUB_REPOSITORY', 'bianhaiming/ai-daily-readings')
    token = os.environ.get('GITHUB_TOKEN')

    if not token:
        print("❌ GITHUB_TOKEN 未设置")
        return

    title = f"📖 每日深度阅读 - {datetime.now().strftime('%Y-%m-%d')}"

    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'title': title,
        'body': content,
        'labels': ['daily-reading', 'ai']
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        issue_url = response.json()['html_url']
        print(f"✅ Issue 创建成功: {issue_url}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 创建 Issue 失败: {e}")


if __name__ == '__main__':
    main()
