@echo off
title ProjetoX Daemon
echo Iniciando Daemon ProjetoX...
start /B /MIN python -m projetox.daemon
echo Daemon iniciado em background.
