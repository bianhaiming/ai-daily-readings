# 🚀 AI 每日深度阅读 - 部署说明

## ✅ 已完成

- ✅ 创建 GitHub 仓库
- ✅ 配置 NVIDIA API Key
- ✅ 实现所有 fetcher 模块
- ✅ 实现 NVIDIA LLM 客户端
- ✅ 实现文章筛选和评分系统
- ✅ 实现 Issue 生成器
- ✅ 实现主协调脚本
- ✅ 创建 GitHub Actions workflow
- ✅ 推送代码到 GitHub
- ✅ 测试核心功能

## 📦 仓库地址

https://github.com/bianhaiming/ai-daily-readings

## 🎯 当前状态

### 已配置
- ✅ NVIDIA API Key（GitHub Secret）
- ✅ 所有核心代码
- ✅ 配置文件

### 需要手动完成

#### 1. 添加 GitHub Actions workflow

由于当前 GitHub token 缺少 `workflow` scope，无法直接推送 workflow 文件。

**步骤：**

```bash
# 1. 重新认证 GitHub CLI
gh auth logout -h github.com -u bianhaiming
gh auth login
```

**在浏览器授权时，确保勾选：**
- ✅ **repo**（完整仓库权限）
- ✅ **workflow**（GitHub Actions workflow 权限）⭐ 关键！
- ✅ **gist**（Gist 管理）
- ✅ **read:org**（组织信息读取）

**完成后：**

```bash
# 2. 创建 .github/workflows 目录
mkdir -p .github/workflows

# 3. 创建 workflow 文件（内容见下方）
# 复制以下内容到 .github/workflows/daily-reading.yml

# 4. 提交并推送
git add .github/workflows/daily-reading.yml
git commit -m "Add GitHub Actions workflow"
git push origin main
```

**workflow 文件内容：**

```yaml
name: Daily AI Readings

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  fetch-and-filter:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run main script
        env:
          NVIDIA_API_KEY: ${{ secrets.NVIDIA_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: python main.py

      - name: Cleanup
        if: always()
        run: |
          echo "Workflow completed"
```

#### 2. 配置数据源（可选）

编辑 `config/sources.json` 来自定义数据源和筛选标准。

**推荐配置：**

```json
{
  "daily_limit": 5,
  "minimum_score": 8.0,
  "llm_provider": "nvidia",
  "sources": {
    "github": {
      "enabled": true,
      "priority": "high",
      "daily_limit": 1,
      "config": {
        "trending_languages": ["python", "typescript", "rust"],
        "topics": ["ai", "llm", "machine-learning"],
        "min_stars": 50,
        "days": 30
      }
    }
  }
}
```

## 🧪 测试运行

### 本地测试

```bash
# 1. 克隆仓库（如果还没有）
git clone https://github.com/bianhaiming/ai-daily-readings.git
cd ai-daily-readings

# 2. 安装依赖
python3 -m pip install -r requirements.txt

# 3. 设置环境变量
export NVIDIA_API_KEY="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"
export GITHUB_TOKEN="your-github-token"

# 4. 运行测试
python3 test.py

# 5. 运行完整脚本
python3 main.py
```

### GitHub Actions 测试

添加 workflow 后，可以手动触发测试：

1. 访问：https://github.com/bianhaiming/ai-daily-readings/actions
2. 选择 "Daily AI Readings" workflow
3. 点击 "Run workflow" 按钮

## 📊 查看结果

### GitHub Issues

每天早上 9 点，系统会自动创建一个新的 GitHub Issue，包含：
- 3-5 篇高质量推荐
- AI 生成的摘要
- 每篇的评分
- 数据统计

访问：https://github.com/bianhaiming/ai-daily-readings/issues

## ⚙️ 配置说明

### 数据源

| 数据源 | 默认状态 | 如何启用 |
|--------|---------|---------|
| GitHub | ✅ 启用 | `sources.github.enabled: true` |
| X (Nitter) | ✅ 启用 | `sources.twitter.enabled: true` |
| arXiv | ✅ 启用 | `sources.arxiv.enabled: true` |
| 技术博客 | ✅ 启用 | `sources.blogs.enabled: true` |
| Hacker News | ✅ 启用 | `sources.hackernews.enabled: true` |

### 筛选标准

- **minimum_score**: 最低 AI 评分（默认 8.0/10）
- **daily_limit**: 每天最多推荐篇数（默认 5 篇）

## 🐛 故障排查

### 问题：NVIDIA API 调用失败

**检查：**
```bash
# 验证 API key
echo $NVIDIA_API_KEY

# 测试 API
curl -X POST "https://integrate.api.nvidia.com/v1/chat/completions" \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"meta/llama-3.1-70b-instruct","messages":[{"role":"user","content":"test"}]}'
```

### 问题：GitHub API 速率限制

**解决方法：**
- 添加 `GITHUB_TOKEN` 环境变量
- 或减少查询频率

### 问题：Nitter 实例不可用

**解决方法：**
- 更换 Nitter 实例
- 或自托管 Nitter 服务

## 📈 成本估算

| 项目 | 月成本 | 说明 |
|-----|--------|------|
| GitHub Actions | $0 | 免费额度 |
| NVIDIA API | $0 | 免费额度（5000 调用/月） |
| 其他 | $0 | 使用免费 API |

**总计：$0/月** ✅

## 🎓 使用教程

### 每日阅读流程

1. **早上 9 点**：自动推送推荐到 GitHub Issues
2. **阅读内容**：点击链接，阅读推荐文章
3. **反馈互动**：在 Issue 下评论、点赞
4. **个性化**：根据反馈调整筛选标准

### 手动触发

需要立即获取推荐？

```bash
# 方法 1：GitHub Actions
# 访问 Actions 页面，点击 "Run workflow"

# 方法 2：本地运行
python3 main.py
```

## 🔄 更新和维护

### 更新数据源

编辑 `config/sources.json` 文件。

### 更新筛选标准

修改 `minimum_score` 或 `daily_limit`。

### 添加新的 fetcher

1. 在 `fetchers/` 目录创建新模块
2. 在 `main.py` 中集成
3. 更新配置文件

## 📞 联系方式

有问题或建议？

- 创建 GitHub Issue
- 或直接评论在每日推荐的 Issue 下

---

**🎉 恭喜！你的 AI 每日深度阅读工具已部署完成！**
