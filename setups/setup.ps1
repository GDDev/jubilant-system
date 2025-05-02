$ErrorActionPreference = "Stop"


$scriptsPath = $PSScriptRoot
$rootPath = Resolve-Path "$scriptsPath\.."

$venvPython = "$rootPath\.venv\Scripts\python.exe"

function Run-SetupScript {
    param (
        [string]$ScriptFile
    )

    $name = Split-Path $ScriptPath -Leaf
    Write-Host "Executando: $name..."
    Start-Sleep -Seconds 5
    Clear-Host

    . $ScriptFile

    $null = Read-Host "Pressione qualquer tecla para continuar."
    Clear-Host
}

try
{
    Get-ChildItem -Path $scriptsPath -Filter "setup_*.ps1" | Sort-Object Name | ForEach-Object {
        Run-SetupScript -ScriptFile $_.FullName
    }
}
catch {
    Write-Host "❌ Erro: $($_.Exception.Message)"
    exit 1
}