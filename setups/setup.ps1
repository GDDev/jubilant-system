. .\setup_venv.ps1

# DATABASE VARIABLES 
$database = Read-Host "Banco de dados a ser usado (mysql+pymysql)" # This project used "mysql+pymysql"
$dbUser = Read-Host "Usuario"
$dbPwd = Read-Host "Senha"
$dbHost = Read-Host "Host" # For testing "localhost"
$dbPort = Read-Host "Porta" # For testing "3306"
$dbName = Read-Host "Nome do banco de dados" # This project used "jubilant"

. .\setup_config_file.ps1

. .\setup_database.ps1

. .\setup_apps.ps1