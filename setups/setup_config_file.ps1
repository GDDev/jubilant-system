Write-Host "Configurando aplicacao..."

$configPath = "..\project\.settings.py"

if (!(Test-Path $configPath)) {
    New-Item -Path $configPath -ItemType "file"

    $lines = @(
        "from os import getenv"
        "DB_TYPE = getenv('FLASK_DB_TYPE') or 'mysql+pymysql'"
        "DB_USER = getenv('FLASK_DB_USER') or 'root'"
        "DB_PWD = getenv('FLASK_DB_PWD') or ''"
        "DB_HOST = getenv('FLASK_DB_HOST') or 'localhost'"
        "DB_PORT = getenv('FLASK_DB_PORT') or '3306'"
        "DB_NAME = getenv('FLASK_DB_NAME') or 'jubilant'"

        "SECRET_KEY = getenv('FLASK_SECRET_KEY')",
        "SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'"
    )

    foreach ($line in $lines) {
        Add-Content -Path $configPath -Value $line
    }
}