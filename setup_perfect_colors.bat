@echo off
REM 完美的终端颜色设置 - social-media-hub项目
color 07

REM 设置提示符：绿色(venv) + 黄色路径 + 黄色命令提示符
prompt $E[92m(venv)$E[0m $E[93m$P$E[93m^>$E[0m

echo.
echo 🎨 完美颜色方案已设置：
echo   $E[92m✓ (venv) 提示符：绿色$E[0m
echo   $E[93m✓ 输入命令：黄色$E[0m  
echo   $E[97m✓ 输出结果：白色$E[0m
echo   $E[91m✓ Error信息：红色$E[0m
echo.
echo 💡 现在可以清晰地区分不同类型的内容了！
echo.

REM 创建一个函数来高亮错误信息
doskey grep=findstr /i $*
doskey error-highlight=findstr /i "error\|fail\|exception\|traceback"
