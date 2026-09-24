# PowerShell deployment script for Windows
param(
    [Parameter(Mandatory=$true)]
    [string]$GithubUsername
)

Write-Host "🚀 MCP Experiments - GitHub + Vercel Deployment" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$RepoName = "MCP-Experiments"
$GithubUrl = "https://github.com/$GithubUsername/$RepoName.git"

Write-Host "📦 Preparing deployment..." -ForegroundColor Yellow
Write-Host "GitHub: $GithubUrl" -ForegroundColor White
Write-Host ""

# Check if git is initialized
if (!(Test-Path ".git")) {
    Write-Host "❌ Git not initialized. Run 'git init' first." -ForegroundColor Red
    exit 1
}

# Add all files
Write-Host "📝 Adding files to git..." -ForegroundColor Yellow
git add -A

# Check for changes
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Committing changes..." -ForegroundColor Yellow
    git commit -m "Prepare for deployment"
} else {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
}

# Check if remote exists
$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Yellow
    git remote add origin $GithubUrl
} else {
    Write-Host "✅ GitHub remote already exists" -ForegroundColor Green
    git remote set-url origin $GithubUrl
}

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin master --force

Write-Host ""
Write-Host "✅ Pushed to GitHub successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://vercel.com" -ForegroundColor White
Write-Host "2. Click 'New Project'" -ForegroundColor White
Write-Host "3. Import: $GithubUrl" -ForegroundColor White
Write-Host "4. Click 'Deploy'" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Your app will be live in minutes!" -ForegroundColor Green
