@echo off
set MSG=%~1
if "%MSG%"=="" set MSG=release checkpoint
scripts\test_push.bat "%MSG%"
