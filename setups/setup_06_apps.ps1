. "$rootPath\.venv\Scripts\Activate.ps1"

Write-Host "Iniciando Not_Found..."
Start-Sleep -Seconds 3
Set-Location "$rootPath"
#Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app.py"
python -m not_found.app

Write-Host "Iniciando aplicacao..."
Start-Sleep -Seconds 3
Set-Location "..\"
python -m project.app