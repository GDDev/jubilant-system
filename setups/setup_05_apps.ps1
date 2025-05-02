Write-Host "Iniciando Not_Found..."
Start-Sleep -Seconds 3
Set-Location "$rootPath\not_found"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app.py"

Write-Host "Iniciando aplicacao..."
Start-Sleep -Seconds 3
Set-Location "$rootPath\"
python -m project.app