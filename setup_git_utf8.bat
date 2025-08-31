@echo off
echo 设置Git UTF-8编码配置...

:: 设置代码页为UTF-8
chcp 65001

:: 设置Git编码配置
git config --global core.quotepath false
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8
git config --global gui.encoding utf-8

:: 设置Windows控制台字体（可选）
echo Git UTF-8编码配置完成！
echo 建议重启终端以确保所有设置生效。

pause
