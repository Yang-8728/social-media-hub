@echo off
REM 增强版日志查看工具 - 自动高亮错误信息
setlocal enabledelayedexpansion

if "%1"=="" (
    echo 用法: view-log.bat [日志文件路径]
    echo 示例: view-log.bat logs\2025-08-25-ai_vanvan.log
    exit /b 1
)

set "logfile=%1"
if not exist "%logfile%" (
    echo $E[91m❌ 日志文件不存在: %logfile%$E[0m
    exit /b 1
)

echo $E[96m📄 查看日志: %logfile%$E[0m
echo $E[96m═══════════════════════════════════════$E[0m

for /f "usebackq delims=" %%a in ("%logfile%") do (
    set "line=%%a"
    
    REM 检查是否包含ERROR关键字
    echo !line! | findstr /i /c:"ERROR" >nul
    if !errorlevel! equ 0 (
        echo $E[91m!line!$E[0m
    ) else (
        REM 检查是否包含SUCCESS关键字
        echo !line! | findstr /i /c:"SUCCESS" >nul
        if !errorlevel! equ 0 (
            echo $E[92m!line!$E[0m
        ) else (
            REM 检查是否包含WARNING关键字
            echo !line! | findstr /i /c:"WARNING" >nul
            if !errorlevel! equ 0 (
                echo $E[93m!line!$E[0m
            ) else (
                echo $E[97m!line!$E[0m
            )
        )
    )
)
