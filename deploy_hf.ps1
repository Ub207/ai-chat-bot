# Hugging Face Space Deploy Script
# Ye script aapke backend ko HF Space me deploy karega

Write-Host "🚀 Hugging Face Space Deployment Script" -ForegroundColor Green
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found. Please install Git first." -ForegroundColor Red
    exit 1
}

# Get current directory
$currentDir = Get-Location
Write-Host "📁 Current directory: $currentDir" -ForegroundColor Cyan

# Check if we're in the HF Space repo
if (Test-Path ".git") {
    Write-Host "✅ Git repository detected" -ForegroundColor Green
} else {
    Write-Host "⚠️  Not in a git repository. Cloning HF Space..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please run these commands manually:" -ForegroundColor Yellow
    Write-Host "  git clone https://huggingface.co/spaces/ubaid-ai/bot" -ForegroundColor White
    Write-Host "  cd bot" -ForegroundColor White
    Write-Host "  Then run this script again from the bot folder" -ForegroundColor White
    exit 1
}

# Check if required files exist
$requiredFiles = @("app_hf.py", "requirements_hf.txt", "Dockerfile", "space.yaml", "backend")
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Some files are missing. Please copy them from D:\ai-chat-bot" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run these commands:" -ForegroundColor Yellow
    Write-Host "  Copy-Item `"D:\ai-chat-bot\app_hf.py`" -Destination . -Force" -ForegroundColor White
    Write-Host "  Copy-Item `"D:\ai-chat-bot\requirements_hf.txt`" -Destination . -Force" -ForegroundColor White
    Write-Host "  Copy-Item `"D:\ai-chat-bot\Dockerfile`" -Destination . -Force" -ForegroundColor White
    Write-Host "  Copy-Item `"D:\ai-chat-bot\space.yaml`" -Destination . -Force" -ForegroundColor White
    Write-Host "  Copy-Item `"D:\ai-chat-bot\backend`" -Destination . -Recurse -Force" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "📦 All required files found!" -ForegroundColor Green
Write-Host ""

# Ask for confirmation
$confirm = Read-Host "Ready to commit and push? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Git add
Write-Host "📝 Adding files to git..." -ForegroundColor Cyan
git add .

# Git commit
Write-Host "💾 Committing changes..." -ForegroundColor Cyan
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Deploy AI Chat Bot backend to Hugging Face"
}
git commit -m $commitMessage

# Git push
Write-Host "🚀 Pushing to Hugging Face..." -ForegroundColor Cyan
git push

Write-Host ""
Write-Host "✅ Deployment initiated!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://huggingface.co/spaces/ubaid-ai/bot" -ForegroundColor White
Write-Host "2. Check the 'Logs' tab to see build progress" -ForegroundColor White
Write-Host "3. Once built, test at: https://ubaid-ai-bot.hf.space/" -ForegroundColor White
Write-Host "4. Set environment variables in Settings → Variables and secrets" -ForegroundColor White
Write-Host ""
