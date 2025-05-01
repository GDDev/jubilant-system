Write-Host "Inicializando aplicacao..."
Start-Sleep -Seconds 2
Clear-Host

. "$rootPath\.venv\Scripts\Activate.ps1"

Write-Host "Iniciando Not_Found..."
Set-Location "$rootPath"
#Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app.py"
python -m not_found.app

Write-Host "Iniciando aplicacao..."
Set-Location "..\"
python -m project.app