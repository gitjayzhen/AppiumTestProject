@echo off
title stopAppiumServer
tasklist /V|find "startAppiumServer">nul
if %errorlevel%==0 (
::关闭appium服务
taskkill /F /IM node.exe
taskkill /F /FI "WINDOWTITLE eq startAppiumServer"
)
taskkill /F /FI "WINDOWTITLE eq stopAppiumServer"