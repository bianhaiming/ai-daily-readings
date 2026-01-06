# 📖 AI 每日深度阅读

每天只推荐 3-5 篇高质量 AI 内容，每篇都值得认真读完。

## ✨ 特性

- 🤖 **AI 智能筛选**：使用 NVIDIA API 对所有内容进行质量评分
- 📊 **多数据源**：GitHub Trending、X (Nitter)、arXiv、技术博客、Hacker News
- 🎯 **质量优先**：每天只推荐 3-5 篇，不追求数量
- 💬 **可交互**：通过 GitHub Issues 进行评论和反馈
- 🆓 **完全免费**：使用免费 API 和 GitHub Actions

## 📦 数据源

| 数据源 | 说明 | 权重 |
|--------|------|------|
| 🛠️ GitHub | 高质量开源项目（AI/ML/开发工具） | ⭐⭐⭐⭐⭐ |
| 💬 X (Nitter) | 专家深度推文线程 | ⭐⭐⭐⭐⭐ |
| 🔬 arXiv | 最新 AI/ML 研究论文 | ⭐⭐⭐⭐ |
| 📝 技术博客 | OpenAI、Anthropic、Google AI 等官方博客 | ⭐⭐⭐⭐ |
| 💻 Hacker News | 高分 AI 相关讨论 | ⭐⭐⭐ |

## 🤖 AI 筛选标准

- 📊 **AI 评分**: ≥ 8.0/10
- 🔬 **技术深度**: ≥ 7.0/10
- ⏰ **时效性**: ≤ 3 天（论文除外）
- ⏱️ **阅读时间**: ≤ 30 分钟

## 🚀 使用方法

### 自动运行

每天早上 9 点自动推送推荐到 GitHub Issues。

### 手动运行

```bash
# 1. 克隆仓库
git clone https://github.com/bianhaiming/ai-daily-readings.git
cd ai-daily-readings

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置环境变量
export NVIDIA_API_KEY="your-nvidia-api-key"
export GITHUB_TOKEN="your-github-token"

# 4. 运行
python main.py
```

### GitHub Actions 手动触发

1. 进入仓库的 Actions 页面
2. 选择 "Daily AI Readings" workflow
3. 点击 "Run workflow" 按钮

## ⚙️ 配置

### 数据源配置

编辑 `config/sources.json` 文件：

```json
{
  "daily_limit": 5,
  "minimum_score": 8.0,
  "sources": {
    "github": {
      "enabled": true,
      "daily_limit": 1,
      "config": {
        "topics": ["ai", "llm", "machine-learning"],
        "min_stars": 100
      }
    }
  }
}
```

### 环境变量

在 GitHub Secrets 中配置：

| 变量名 | 说明 | 获取方式 |
|---------|------|---------|
| `NVIDIA_API_KEY` | NVIDIA API Key | https://build.nvidia.com |
| `GITHUB_TOKEN` | GitHub Token | `gh auth login` |

## 📊 示例 Issue

![示例 Issue](https://example.com/screenshot.png)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
