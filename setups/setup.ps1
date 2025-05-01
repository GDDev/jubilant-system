$ErrorActionPreference = "Stop"


$scriptsPath = $PSScriptRoot
$rootPath = Resolve-Path "$scriptsPath\.."

$venvPython = "$rootPath\.venv\Scripts\python.exe"

try
{
    . $scriptsPath\setup_venv.ps1
    Start-Sleep -Seconds 1
    Clear-Host

    . $scriptsPath\setup_env_variables.ps1
    Start-Sleep -Seconds 1
    Clear-Host

    . $scriptsPath\setup_config_file.ps1
    Start-Sleep -Seconds 1
    Clear-Host

    . $scriptsPath\setup_database.ps1
    Start-Sleep -Seconds 1
    Clear-Host

    . $scriptsPath\setup_apps.ps1
    Start-Sleep -Seconds 1
    Clear-Host
}
catch {
    Write-Host "❌ Erro: $($_.Exception.Message)"
    exit 1
}