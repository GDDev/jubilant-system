$secretKey = python -c "import secrets; print(str(secrets.token_hex()))"

$configPath = ".\.settings.cfg"

if (-Not (Test-Path $configPath)) {
    New-Item -Path $configPath -ItemType "file"
}

$secretKeyLine = "SECRET_KEY = '$secretKey'"
Add-Content -Path $configPath -Value $secretKeyLine

$env:FLASK_CONFIG_PATH = $configPath