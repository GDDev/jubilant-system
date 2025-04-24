. ..\.venv\Scripts\activate

Write-Host "Iniciando Not_Found..."
Set-Location "..\not_found"
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "app.py"

Write-Host "Iniciando aplicacao..."
Set-Location "..\"
python -m project.app