@echo off
REM 设置UTF-8编码和绿色(venv)提示符 + 黄色路径
chcp 65001 >nul
color 07
prompt $E[92m(venv)$E[0m $E[93m$P$E[0m^>
echo 🟢 绿色(venv)提示符已设置！
echo 🟡 黄色文件夹路径已设置！
echo 🔤 UTF-8编码已设置！
