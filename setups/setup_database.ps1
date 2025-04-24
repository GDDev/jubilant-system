# Finding MySQL installation
Write-Host "Procurando instalacao do MySQL..."
 $mysqlPaths = Get-ChildItem -Recurse -Filter "mysql.exe" -File -Path "C:\" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName

 Write-Host $mysqlPaths.Count " instalacao(oes) encontradas."

 if (!$mysqlPaths) {
     Write-Host "Esta aplicacao utiliza MySQL, por favor instalar."
     exit 1
 }

 foreach ($path in $mysqlPaths) {
     $chosenPath = Split-Path -Path $path
     if ($chosenPath -eq "C:\xampp\mysql\bin"){
         break # Prioritize XAMPP
     }
 }

# Checking if MySQL is up and running
 Write-Host "Checando inicializacao do MySQL..."
 $mysqlService = Get-Service | Where-Object { $_.Name -match "mysql" }

 if ($mysqlService.Status -ne "Running"){
    Write-Host "Incializando o MySQL..."
#    Start-Service -Name $mysqlService.Name
    Start-Process -FilePath "$chosenPath\mysqld.exe" -NoNewWindow -PassThru
 } else {
     Write-Host "Erro ao inicializar o MySQL."
     exit 1
 }

# Creating database
Write-Host "Criando o banco de dados da aplicacao..."

& "$chosenPath\mysql.exe" -u $dbUser -p $dbPwd -e "CREATE DATABASE IF NOT EXISTS $dbName;"

Set-Location "..\project"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Set-Location "..\setups"