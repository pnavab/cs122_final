@echo off

REM Add the current directory to the user PATH if it is not already there
for /f "usebackq tokens=2,*" %%A in (`reg query HKCU\Environment /v PATH`) do set my_user_path=%%B

echo.%my_user_path% | findstr /C:"%cd%" 1>nul
if errorlevel 1 (
  setx PATH "%my_user_path%;%cd%"
) else (
  echo The current directory is already in the PATH.
)

echo DIRECTORY=%cd% > .env
echo {} > pi.json