Write-Host "Checando instalacao do Python..."
Start-Sleep -Seconds 3
If (!(Get-Command python -ErrorAction SilentlyContinue)){
    throw "Esta é uma aplicacao Python, portanto Python deve estar instalado para roda-la."
}

Set-Location $rootPath

Write-Host "Checando existencia de um ambiente virtual..."
Start-Sleep -Seconds 3
if (!(Test-Path "$rootPath\.venv\")){
    Write-Host "Nenhum ambiente virtual encontrado.`nGerando ambiente virtual..."
    Start-Sleep -Seconds 3
    python -m venv .\.venv
    . "$rootPath\.venv\Scripts\Activate.ps1"
}

Write-Host "Checando ativacao do ambiente virtual..."
Start-Sleep -Seconds 3
if ((& $venvPython -c "import sys; print(sys.prefix)") -match ".*\\.venv") {
    Write-Host "Instalando dependencias..."
    Start-Sleep -Seconds 3
    & $venvPython -m pip install -r $rootPath\requirements.txt
}
else{
    throw "Erro ao ativar ambiente virtual."
}