Write-Host "Configurando aplicacao..."

$configPath = "..\project\.settings.py"

if (!(Test-Path $configPath)) {
    New-Item -Path $configPath -ItemType "file"

    $lines = @(
        "import os"
        "DB_TYPE = os.getenv('FLASK_DB_TYPE')"
        "DB_USER = os.getenv('FLASK_DB_USER')"
        "DB_PWD = os.getenv('FLASK_DB_PWD')"
        "DB_HOST = os.getenv('FLASK_DB_HOST')"
        "DB_PORT = os.getenv('FLASK_DB_PORT')"
        "DB_NAME = os.getenv('FLASK_DB_NAME')"

        "SECRET_KEY = os.getenv('FLASK_SECRET_KEY')",
        "SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'"
    )

    foreach ($line in $lines) {
        Add-Content -Path $configPath -Value $line
    }
}