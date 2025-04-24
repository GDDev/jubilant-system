Write-Host "Configurando aplicacao..."

$configPath = "..\project\.settings.cfg"

$secretKey = python -c "import secrets; print(str(secrets.token_hex()))"
if (!(Test-Path $configPath)) {
    New-Item -Path $configPath -ItemType "file"

    $lines = @(
        "SECRET_KEY = '${secretKey}'",
        "SQLALCHEMY_DATABASE_URI = '${database}://${dbUser}:${dbPwd}@${dbHost}:${dbPort}/${dbName}'"
    )

    foreach ($line in $lines) {
        Add-Content -Path $configPath -Value $line
    }
}

$env:FLASK_CONFIG_PATH = $configPath