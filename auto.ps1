param([string]$task)
if (-not $task) {
    Write-Host "Usage: .\auto.ps1 your task"
    exit
}

$model = "qwen2.5:3b"
$apiUrl = "http://localhost:11434/api/generate"
$githubUser = "1427993681"

$promptText = @"
You are a PowerShell script generator. Output ONLY executable commands, one per line.
Rules:
- Use a unique repository name based on the task (e.g., my-flask-app, health-api). NEVER use placeholders like NAME or USER.
- Use Set-Content to create files, Add-Content to append.
- Always create Flask apps starting with:
  Set-Content -Path app.py -Value "from flask import Flask"
  Add-Content -Path app.py -Value "app = Flask(__name__)"
- For requirements.txt, write: Set-Content -Path requirements.txt -Value "flask"; Add-Content -Path requirements.txt -Value "pytest"
- Create and activate venv: python -m venv .venv; .\.venv\Scripts\Activate.ps1
- Install dependencies: pip install -r requirements.txt
- Before creating a repo, set a variable: `$repoName = "your-chosen-name"`
- Delete existing repo (ignore errors): gh repo delete $repoName --yes 2>`$null
- Create and push: gh repo create $repoName --public --source=. --remote=origin --push
- If origin remote exists, update it: git remote set-url origin https://github.com/$githubUser/`$repoName.git
- Always add and commit before pushing: git add .; git commit -m "Initial commit"
- Use git push -u origin master
- Do NOT use Linux syntax like 2>/dev/null. Use 2>`$null for PowerShell.
Now generate commands for this task:
"@

$fullPrompt = "$promptText`n`nTask: $task"
$body = @{model=$model;prompt=$fullPrompt;stream=$false} | ConvertTo-Json

Write-Host "Consulting local brain..."
try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "application/json" -TimeoutSec 600
} catch {
    Write-Host "Connection failed: $_"
    exit 1
}

$raw = $response.response.Trim()
$commands = @()
foreach ($line in ($raw -split "`n")) {
    $clean = $line.Trim()
    if ($clean -match '^(New-Item|cd |mkdir |python |pip |Set-Content|Add-Content|Out-File|echo |git |gh |pytest |start |\$repoName|\.\\\.venv|\.\\venv|venv\\|@'')') {
        $commands += $clean
    }
}

if (-not $commands) {
    Write-Host "No commands extracted. Raw:"
    Write-Host $raw
    exit 1
}

Write-Host "`nCommands:"
Write-Host ($commands -join "`n")
$confirm = Read-Host "`nExecute? (y/n)"
if ($confirm -ne "y") { exit }

foreach ($cmd in $commands) {
    Write-Host "`n> $cmd"
    try {
        Invoke-Expression $cmd
    } catch {
        Write-Host "Error: $_"
    }
}

# Run tests if available
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    if (Get-ChildItem -Path . -Filter "test_*.py" -Recurse) {
        Write-Host "`nRunning tests..."
        .\.venv\Scripts\Activate.ps1
        pytest
    }
}

Write-Host "`nDone."