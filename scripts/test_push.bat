@echo off
setlocal enabledelayedexpansion

REM Usage:
REM   scripts\test_push.bat "commit message"
REM If no message is supplied, a timestamped message is used.

set MSG=%~1
if "%MSG%"=="" set MSG=Auto checkpoint after passing pytest

echo.
echo === Running pytest ===
python -m pytest
if errorlevel 1 (
    echo.
    echo TESTS FAILED - not committing or pushing.
    exit /b 1
)

echo.
echo === Tests passed. Checking git status ===
git status --short

echo.
echo === Staging changes ===
git add -A

git diff --cached --quiet
if %errorlevel%==0 (
    echo No staged changes to commit.
    exit /b 0
)

echo.
echo === Committing ===
git commit -m "%MSG%"
if errorlevel 1 (
    echo Commit failed.
    exit /b 1
)

echo.
echo === Pushing to GitHub ===
git push
if errorlevel 1 (
    echo Push failed. Check remote/authentication.
    exit /b 1
)

echo.
echo SUCCESS: tests passed, changes committed, pushed to GitHub.
