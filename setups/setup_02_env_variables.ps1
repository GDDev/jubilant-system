Set-Location $rootPath

Write-Host "Definindo variaves do banco de dados..."
Start-Sleep 3
$env:FLASK_DB_TYPE = Read-Host "Banco de dados a ser usado (padrao: mysql+pymysql)"
if (-Not $env:FLASK_DB_TYPE){
    $env:FLASK_DB_TYPE = "mysql+pymysql"
}
$env:FLASK_DB_USER = Read-Host "Usuario (padrao: root)"
if (-Not $env:FLASK_DB_USER){
    $env:FLASK_DB_USER = "root"
}
$env:FLASK_DB_PWD = Read-Host "Senha"
if (-Not $env:FLASK_DB_PWD){
    $env:FLASK_DB_PWD = ""
}
$env:FLASK_DB_HOST = Read-Host "Host (padrao: localhost)"
if (-Not $env:FLASK_DB_HOST){
    $env:FLASK_DB_HOST = "localhost"
}
$env:FLASK_DB_PORT = Read-Host "Porta (padrao: 3306)"
if (-Not $env:FLASK_DB_PORT){
    $env:FLASK_DB_PORT = "3306"
}
$env:FLASK_DB_NAME = Read-Host "Nome do banco de dados (padrao: jubilant)"
if (-Not $env:FLASK_DB_NAME){
    $env:FLASK_DB_NAME = "jubilant"
}
Start-Sleep -Seconds 2
Clear-Host

Write-Host "Gerando FLASK_SECRET_KEY..."
Write-Host $PWD
Start-Sleep 3
if (-Not $env:FLASK_SECRET_KEY){
    $secretKey = python -c "from secrets import token_hex; print(str(token_hex()))"
    if (-Not $secretKey){
        throw "Falha ao gerar Chave Secreta."
    }
    Write-Host $secretKey
    $env:FLASK_SECRET_KEY = $secretKey
    Write-Host "FLASK_SECRET_KEY gerada com sucesso."
    Write-Host "Flask_SECRET_KEY: " $env:FLASK_SECRET_KEY
    Start-Sleep 3
}
else {
    Write-Host "FLASK_SECRET_KEY ja definida..."
}

$envPath = "$rootPath\.env"
Write-Host "Checando existencia de um arquivo .env..."
Start-Sleep 3
if (-Not (Test-Path $envPath)){
    Write-Host "Criando arquivo .env..."
    Start-Sleep 3
    New-Item -Path $envPath -ItemType "file" | Out-Null
    if (-Not (Test-Path $envPath)){
        throw "Nao foi possivel criar o arquivo .env."
    }
    Write-Host "Checando existencia de uma chave mestra de criptografia..."
    Start-Sleep 3
    if (-Not (Test-Path Env:JUBILANT_MASTER_KEY)) {
        Write-Host "Gerando uma nova chave de criptografia..."
        Start-Sleep 3
        $fernetKey = python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
        if (-Not $fernetKey){
            throw "Falha ao gerar Chave Mestra de Criptografia."
        }
        $env:JUBILANT_MASTER_KEY = $fernetKey
        setx JUBILANT_MASTER_KEY $fernetKey
        Write-Host "JUBILANT_MASTER_KEY gerada com sucesso."
        Start-Sleep 3

    } else {
        Write-Host "A chave de criptografia JUBILANT_MASTER_KEY ja existe. Nenhuma nova chave foi gerada."
    }

    Write-Host "Configurando a chave de criptografia JUBILANT_MASTER_KEY..."
    Start-Sleep 3
    Set-Content -Path $envPath -Value "JUBILANT_MASTER_KEY=$fernetKey"
}
else{
    Write-Host "Arquivo .env ja existente."
    Start-Sleep 3
}