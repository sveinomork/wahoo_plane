# Requires PowerShell 5.1 or later (standard on modern Windows)

$repoUrl = "https://github.com/sveinomork/wahoo_plane.git"
$installDir = "$env:LOCALAPPDATA\WahooPlaneCLI"
$binDir = "$env:LOCALAPPDATA\Microsoft\WindowsApps" # Common location for user apps in PATH

Write-Host "Starting Wahoo Plane CLI installation..." -ForegroundColor Green

# --- Check for Git ---
Write-Host "Checking for Git..."
try {
    git --version | Out-Null
} catch {
    Write-Host "Git is not installed or not in PATH. Please install Git from https://git-scm.com/ and try again." -ForegroundColor Red
    exit 1
}

# --- Check for uv (Rye) ---
Write-Host "Checking for uv (Rye)..."
try {
    uv --version | Out-Null
} catch {
    Write-Host "uv (Rye) is not installed. Please install it first: https://rye-up.com/guide/installation/" -ForegroundColor Red
    Write-Host "Alternatively, you can modify this script to use 'python -m venv' and 'pip install'." -ForegroundColor Yellow
    exit 1
}

# --- Clone or Update Repository ---
if (Test-Path $installDir) {
    Write-Host "Wahoo Plane repository already exists at $installDir. Updating..." -ForegroundColor Yellow
    try {
        Push-Location $installDir
        git pull
        Pop-Location
    } catch {
        Write-Host "Failed to update repository. Please check permissions or delete '$installDir' and try again." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Cloning Wahoo Plane repository into $installDir..." -ForegroundColor Green
    try {
        git clone $repoUrl $installDir
    } catch {
        Write-Host "Failed to clone repository. Exiting." -ForegroundColor Red
        exit 1
    }
}

# --- Navigate to Installation Directory ---
Set-Location $installDir -ErrorAction Stop
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to change directory to $installDir. Exiting." -ForegroundColor Red
    exit 1
}

# --- Create and Install Virtual Environment ---
Write-Host "Setting up virtual environment and installing dependencies..." -ForegroundColor Green
try {
    uv venv
    # Activate venv for the current PowerShell session
    . .\.venv\Scripts\Activate.ps1
    uv pip install -e .
} catch {
    Write-Host "Failed to set up virtual environment or install dependencies. Exiting." -ForegroundColor Red
    exit 1
}

# --- Create Wrapper .cmd file ---
Write-Host "Creating wrapper for 'wahoo' command..." -ForegroundColor Green
$wrapperContent = @"
@echo off
CALL "$installDir\.venv\Scripts\activate.bat"
wahoo %*
"@

$wrapperPath = Join-Path $binDir "wahoo.cmd"
try {
    New-Item -ItemType Directory -Path $binDir -ErrorAction SilentlyContinue | Out-Null
    Set-Content -Path $wrapperPath -Value $wrapperContent -Force
} catch {
    Write-Host "Failed to create wrapper script at $wrapperPath. You may need to add '$installDir\.venv\Scripts' to your PATH manually." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Wahoo Plane CLI installed successfully!" -ForegroundColor Green
Write-Host "You can now run 'wahoo' from any Command Prompt or PowerShell window." -ForegroundColor Green
Write-Host "You might need to restart your terminal for changes to take effect." -ForegroundColor Yellow
Write-Host ""