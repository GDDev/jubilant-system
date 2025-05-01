Write-Host "Gerando ambientes e dependencias..."
Start-Sleep -Seconds 2
Clear-Host

Write-Host "Checando instalacao do Python..."
If (!(Get-Command python -ErrorAction SilentlyContinue)){
    throw "Esta é uma aplicacao Python, portanto Python deve estar instalado para roda-la."
}

Set-Location $rootPath

Write-Host "Checando existencia de um ambiente virtual..."
if (!(Test-Path "$rootPath\.venv\")){
    Write-Host "Nenhum ambiente virtual encontrado.`n Gerando ambiente virtual..."
    python -m venv .\.venv
    . "$rootPath\.venv\Scripts\Activate.ps1"
}

Write-Host "Checando ativacao do ambiente virtual..."
if ((& $venvPython -c "import sys; print(sys.prefix)") -match ".*\\.venv") {
    Write-Host "Instalando dependencias..."
    & $venvPython -m pip install -r $rootPath\requirements.txt
}
else{
    throw "Erro ao ativar ambiente virtual."
}