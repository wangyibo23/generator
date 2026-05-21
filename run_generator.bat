@echo off
chcp 65001 >nul 2>nul
title Keyboard Config Code Generator
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 py 命令，请安装 py 并确保添加到 PATH。
    pause
    exit /b 1
)

py --version

:: 检查 jinja2，使用 py -c 导入
py -c "import jinja2" >nul 2>nul
if %errorlevel% neq 0 (
    echo [警告] 缺少 jinja2 模块，尝试使用 py -m pip 安装...
    py -m pip install jinja2
    if %errorlevel% neq 0 (
        echo [错误] 安装 jinja2 失败，请手动执行: py -m pip install jinja2
        pause
        exit /b 1
    )
)

echo 正在生成 C 代码...
py code_generator.py
if %errorlevel% neq 0 (
    echo [错误] 脚本执行失败
    pause
    exit /b %errorlevel%
)

echo 成功生成代码，输出文件位于 generated\ 目录下。
pause