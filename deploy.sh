#!/bin/bash

echo "🚀 AI 每日深度阅读 - 完整部署脚本"
echo ""

# 1. 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 未登录 GitHub CLI"
    echo "请先运行: gh auth login"
    exit 1
fi

echo "✅ 已登录到 GitHub"
echo ""

# 2. 检查 workflow 权限
SCOPES=$(gh auth status 2>&1 | grep "Token scopes:" | sed 's/.*: //' | tr -d "'")
echo "📋 当前 Token Scopes: $SCOPES"
echo ""

if [[ ! "$SCOPES" =~ "workflow" ]]; then
    echo "⚠️  缺少 workflow 权限"
    echo "请运行: gh auth refresh -h github.com -s workflow"
    echo ""
    read -p "按回车键继续（假设你有 workflow 权限）..."
fi

# 3. 设置远程 URL（带 token）
REPO="bianhaiming/ai-daily-readings"
TOKEN=$(gh auth token)

echo "🔧 配置 Git 远程..."
git remote set-url origin https://x-access-token:$TOKEN@github.com/$REPO.git

# 4. 提交并推送
echo ""
echo "📝 提交 workflow 文件..."
git add .github/workflows/daily-reading.yml

if git diff --cached --quiet; then
    echo "ℹ️  没有需要提交的更改"
else
    git commit -m "Add GitHub Actions workflow"

    echo "📤 推送到 GitHub..."
    git push origin main
fi

# 5. 恢复远程 URL
git remote set-url origin https://github.com/$REPO.git

echo ""
echo "✅ 部署完成！"
echo ""
echo "📌 下一步："
echo "1. 访问: https://github.com/$REPO/actions"
echo "2. 手动触发 workflow 进行测试"
echo "3. 查看生成的 Issues: https://github.com/$REPO/issues"
echo ""
