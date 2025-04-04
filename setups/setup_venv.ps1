Write-Host "Gerando ambientes e dependencias..."

# Check Python installation
If (!(Get-Command python -ErrorAction SilentlyContinue)){
    Write-Host "Esta é uma aplicacao Python, portanto Python deve estar instalado para roda-la."
    exit 1
}

# Create virtual environment
if (!(Test-Path "..\.venv") -and !(Test-Path "..\venv") -and !(Test-Path "..\env")){
    python -m venv ..\.venv
}

# Activating virtual environment
if ($env:ComSpec -match "cmd.exe") {
    cmd /c "..\.venv\Scripts\activate.bat"
} else {
    . ..\.venv\Scripts\activate
}

# Installing dependencies
# Ensure the virtual environment is actually activated
$venvPython = "..\.venv\Scripts\python.exe"

# Check if Python from .venv is running, not the system one
if ((& $venvPython -c "import sys; print(sys.prefix)") -match ".*\\.venv") {
    # Now install requirements in the correct environment
    & $venvPython -m pip install -r ..\requirements.txt
}