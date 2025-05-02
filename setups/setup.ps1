$ErrorActionPreference = "Stop"


$scriptsPath = $PSScriptRoot
$rootPath = Resolve-Path "$scriptsPath\.."

$venvPython = "$rootPath\.venv\Scripts\python.exe"

function Run-SetupScript {
    param (
        [string]$ScriptFile
    )

    try {
        if (-not (Test-Path $ScriptFile)) {
            throw "Arquivo de script nao encontrado: $ScriptFile"
        }

        $name = Split-Path $ScriptFile -Leaf
        Write-Host "Executando: $name..."
        Start-Sleep -Seconds 5
        Clear-Host

        . $ScriptFile

        $null = Read-Host "Pressione ENTER para continuar"
        Clear-Host
        }
    catch {
        throw "Erro ao executar o script: $_"
    }

}

try
{
    Get-ChildItem -Path $scriptsPath -Filter "setup_*.ps1" | Sort-Object Name | ForEach-Object {
        Run-SetupScript -ScriptFile $_.FullName
    }
}
catch {
    Write-Host "[ERRO] Erro: $($_.Exception.Message)"
    exit 1
}