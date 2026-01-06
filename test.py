import os
import json
from fetchers.github_fetcher import GitHubFetcher
from llm.nvidia_client import NvidiaClient


def test_github_fetcher():
    """测试 GitHub fetcher"""
    config = {
        'trending_languages': ['python'],
        'topics': [],
        'min_stars': 10,
        'days': 30
    }

    fetcher = GitHubFetcher(config)
    projects = fetcher.fetch_trending()

    print(f"✓ 获取了 {len(projects)} 个 GitHub 项目")

    if projects:
        project = projects[0]
        print(f"✓ 示例项目: {project['title']}")
        print(f"  Stars: {project['stars']}")
        print(f"  URL: {project['url']}")


def test_nvidia_client():
    """测试 NVIDIA 客户端"""
    api_key = os.environ.get('NVIDIA_API_KEY')

    if not api_key:
        print("❌ NVIDIA_API_KEY 未设置")
        return

    try:
        client = NvidiaClient(api_key)
        response = client.chat("Hello, please say 'Test successful!'")
        print(f"✓ NVIDIA API 响应: {response}")
    except Exception as e:
        print(f"❌ NVIDIA API 测试失败: {e}")


def main():
    print("🧪 开始测试...\n")

    print("1. 测试 NVIDIA 客户端...")
    test_nvidia_client()

    print("\n2. 测试 GitHub fetcher...")
    test_github_fetcher()

    print("\n✅ 测试完成！")


if __name__ == '__main__':
    main()
