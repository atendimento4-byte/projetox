@echo off
REM ProjetoX — Launcher
REM Fixa PYTHONPATH e carrega variaveis de ambiente

setlocal
set PYTHONPATH=
set "PROJETOX_DIR=%~dp0"

REM Carregar .env se existir
if exist "%PROJETOX_DIR%.env" (
    for /f "tokens=1,* delims==" %%a in ('type "%PROJETOX_DIR%.env" ^| findstr /v "^#"') do (
        if not "%%a"=="" set "%%a=%%b"
    )
)

REM Executar comando
if "%1"=="" (
    echo ProjetoX — Assistente Inteligente de Atendimentos
    echo.
    echo Uso: run-projetox.cmd --help
    echo      run-projetox.cmd acompanhamento iniciar ^<chamado^> ^<cliente^>
    echo.
    "%PROJETOX_DIR%.venv\Scripts\python.exe" -m projetox --help
) else (
    "%PROJETOX_DIR%.venv\Scripts\python.exe" -m projetox %*
)

endlocal
