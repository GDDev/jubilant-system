Write-Host "Configurando variaveis de ambiente..."

# DATABASE VARIABLES
$env:FLASK_DB_TYPE = Read-Host "Banco de dados a ser usado (mysql+pymysql)"
$env:FLASK_DB_USER = Read-Host "Usuario"
$env:FLASK_DB_PWD = Read-Host "Senha"
$env:FLASK_DB_HOST = Read-Host "Host (localhost)"
$env:FLASK_DB_PORT = Read-Host "Porta (3306)"
$env:FLASK_DB_NAME = Read-Host "Nome do banco de dados (jubilant)"

$secretKey = python -c "import secrets; print(str(secrets.token_hex()))"
$env:FLASK_SECRET_KEY = $secretKey