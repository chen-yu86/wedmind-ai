# -------------------------------
# WedMind AI 一鍵部署腳本
# -------------------------------

# 1️⃣ 進入專案資料夾
$projectPath = "C:\軟體\程式語言學習\text2026\WedMind"
cd $projectPath

# 2️⃣ 安裝必要套件
Write-Host "Step 1: 安裝套件..."
pip install --upgrade pip
pip install -r requirements.txt

# 3️⃣ 初始化 Git（第一次使用）
if (-not (Test-Path ".git")) {
    Write-Host "Step 2: 初始化 Git..."
    git init
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git remote add origin https://github.com/chen-yu86/wedmind-ai.git 2>$null
}

# 更新遠端 URL
git remote set-url origin https://github.com/chen-yu86/wedmind-ai.git

# 4️⃣ Git commit & push
Write-Host "Step 3: 提交並推送到 GitHub..."
git add .
$commitMessage = Read-Host "請輸入 commit 訊息"
git commit -m $commitMessage
git branch -M main
git push -u origin main

Write-Host "✅ 已成功推送到 GitHub！Render 將自動部署網站。"
Write-Host "請到 Render 監控部署狀態。"