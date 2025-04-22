. ..\.venv\Scripts\activate

Write-Host "Iniciando Not_Found..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "..\not_found\app.py"

Write-Host "Iniciando aplicacao..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "..\project\app.py"