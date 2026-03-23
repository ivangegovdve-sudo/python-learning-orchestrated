@echo off
echo Starting Python Learning App...
echo Syncing dependencies...
call uv sync --group dev
if %errorlevel% neq 0 (
    echo Error syncing dependencies. Make sure 'uv' is installed.
    pause
    goto :eof
)

echo Launching app...
call uv run python-learning session
if %errorlevel% neq 0 (
    pause
)
