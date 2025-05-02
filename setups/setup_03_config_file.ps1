$configPath = "$rootPath\project\.settings.py"

Write-Host "Checando existencia do arquivo de configuracao da aplicacao..."
Start-Sleep -Seconds 3
if (!(Test-Path $configPath)) {
    Write-Host "Criando arquivo de configuracao..."
    Start-Sleep -Seconds 3
    New-Item -Path $configPath -ItemType "file"

    if(-Not (Test-Path $configPath)){
        throw "Nao foi possivel criar o arquivo de configuracao."
    }
    Write-Host "Arquivo de configuracao criado.`nPopulando configuracoes..."
    Start-Sleep -Seconds 3
    $lines = @(
        "from os import getenv"
        "DB_TYPE = getenv('FLASK_DB_TYPE')"
        "DB_USER = getenv('FLASK_DB_USER')"
        "DB_PWD = getenv('FLASK_DB_PWD') or ''"
        "DB_HOST = getenv('FLASK_DB_HOST')"
        "DB_PORT = getenv('FLASK_DB_PORT')"
        "DB_NAME = getenv('FLASK_DB_NAME')"

        "SECRET_KEY = getenv('FLASK_SECRET_KEY')",
        "SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'"
    )
    foreach ($line in $lines) {
        Add-Content -Path $configPath -Value $line
    }
    Write-Host "Arquivo de configuracao populado com sucesso."
    Start-Sleep -Seconds 3
}