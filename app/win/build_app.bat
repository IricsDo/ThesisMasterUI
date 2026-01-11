@echo off
setlocal

set "PROJ=E:\Work Spaces\Thesis\Code\ThesisMasterUI\ThesisMasterUI_Tkinter"

set "BASE=E:\Work Spaces\Thesis\Code\ThesisMasterUI\app\win\builds"
set "DIST=%BASE%\dist"
set "WORK=%BASE%\work"
set "SPEC=%BASE%\spec"

pyinstaller --noconfirm --clean --onefile --console ^
  --debug imports ^
  --name DeePMD-Kit ^
  --icon "%PROJ%\images\ai_64.ico" ^
  --add-data "%PROJ%\images;images" ^
  --distpath "%DIST%" ^
  --workpath "%WORK%" ^
  --specpath "%SPEC%" ^
  "E:\Work Spaces\Thesis\Code\ThesisMasterUI\ThesisMasterUI_Tkinter\app.py"

if errorlevel 1 (
    echo Build failed with error code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

echo Build succeeded. Output: "%DIST%\DeePMD-Kit.exe"
endlocal
