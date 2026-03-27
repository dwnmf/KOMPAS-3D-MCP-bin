@echo off
setlocal

set "REPO_ROOT=%~dp0"
cd /d "%REPO_ROOT%"

if "%~1"=="" goto usage

set "RELEASE_TAG=%~1"
set "SOURCE_ZIP=%REPO_ROOT%kompasmcp.zip"
set "OUTPUT_DIR=%REPO_ROOT%build\release"
set "ASSET_PATH=%OUTPUT_DIR%\KOMPAS-3D-MCP-bin-%RELEASE_TAG%.zip"
set "RELEASE_NOTES=%TEMP%\kompas-mcp-release-notes-%RANDOM%.md"

if not exist "%SOURCE_ZIP%" (
  echo Source zip not found: %SOURCE_ZIP%
  exit /b 1
)

echo Building final client package...
python scripts\package_client_release.py --source-zip "%SOURCE_ZIP%" --output-dir "%OUTPUT_DIR%" --version-label "%RELEASE_TAG%"
if errorlevel 1 exit /b 1

if not exist "%ASSET_PATH%" (
  echo Final asset not found: %ASSET_PATH%
  exit /b 1
)

(
  echo Ready-to-use Windows package for KOMPAS-3D MCP.
  echo.
  echo Included:
  echo - kompas-mcp.exe
  echo - runtime files
  echo - installation README
  echo - kompas-mcp-operator skill
  echo.
  echo This repository does not publish application source code.
) > "%RELEASE_NOTES%"

echo Publishing %ASSET_PATH% to release %RELEASE_TAG%...
gh release view "%RELEASE_TAG%" --repo dwnmf/KOMPAS-3D-MCP-bin >nul 2>&1
if errorlevel 1 (
  gh release create "%RELEASE_TAG%" "%ASSET_PATH%" --repo dwnmf/KOMPAS-3D-MCP-bin --title "%RELEASE_TAG%" --notes-file "%RELEASE_NOTES%"
) else (
  gh release upload "%RELEASE_TAG%" "%ASSET_PATH%" --repo dwnmf/KOMPAS-3D-MCP-bin --clobber
  if errorlevel 1 goto fail
  gh release edit "%RELEASE_TAG%" --repo dwnmf/KOMPAS-3D-MCP-bin --title "%RELEASE_TAG%" --notes-file "%RELEASE_NOTES%"
)
if errorlevel 1 goto fail

del "%RELEASE_NOTES%" >nul 2>&1
echo Done.
echo https://github.com/dwnmf/KOMPAS-3D-MCP-bin/releases/tag/%RELEASE_TAG%
exit /b 0

:usage
echo Usage: publish_client_release.bat v1.0.16
exit /b 1

:fail
del "%RELEASE_NOTES%" >nul 2>&1
echo Release publish failed.
exit /b 1
