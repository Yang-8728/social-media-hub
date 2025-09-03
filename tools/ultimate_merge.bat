@echo off
chcp 65001 > nul
echo 🎯 终极视频合并工具
echo ==================

if "%1"=="" (
    echo ❌ 请指定账户名
    echo 💡 使用方法: ultimate_merge.bat ai_vanvan
    pause
    exit /b 1
)

echo 🚀 开始终极标准化合并: %1
echo 📋 功能包括:
echo   - 修复负数时间戳
echo   - 统一音频质量为128kbps
echo   - 标准化所有编码参数
echo   - 安全合并避免卡顿

python main.py --merge %1 --ultimate

echo.
echo ✅ 合并完成！
pause
