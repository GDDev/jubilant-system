Write-Host "Configurando banco de dados..."
Start-Sleep -Seconds 2
Clear-Host

Write-Host "Procurando instalacao do MySQL..."
$mysqlPaths = Get-ChildItem -Recurse -Filter "mysql.exe" -File -Path "C:\" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName

Write-Host $mysqlPaths.Count " instalacao(oes) encontradas."

if (!$mysqlPaths) {
    throw "Esta aplicacao utiliza o banco de dados MySQL, por favor instale-o."
}

foreach ($path in $mysqlPaths) {
    $chosenPath = Split-Path -Path $path
    if ($chosenPath -eq "C:\xampp\mysql\bin"){
        break # Prioritize XAMPP
    }
}

Write-Host "Checando inicializacao do MySQL..."
$mysqlService = Get-Service | Where-Object { $_.Name -match "mysql" }

if ($mysqlService.Status -ne "Running"){
    Write-Host "Incializando o MySQL..."
    Start-Process -FilePath "$chosenPath\mysqld.exe" -NoNewWindow -PassThru

    if ($mysqlService.Status -ne "Running"){
        throw "Erro ao inicializar o MySQL."
    }
} else {
    Write-Host "MySQL já inicializado..."
}

Write-Host "Criando o banco de dados $env:FLASK_DB_NAME..."
& "$chosenPath\mysql.exe" -u $env:FLASK_DB_USER -p $env:FLASK_DB_PWD -e "CREATE DATABASE IF NOT EXISTS $env:FLASK_DB_NAME;"

Write-Host "Iniciando migracoes..."
Set-Location "$rootPath\project"
& $venvPython flask db upgrade