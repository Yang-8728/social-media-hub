@echo off
chcp 65001 > nul
echo 🎬 视频质量分析工具
echo ================

echo 📊 扫描所有视频音频质量...
python scripts/analysis/complete_audio_scan.py

echo.
echo ✅ 分析完成！
echo 💡 如果发现问题视频，建议使用终极合并模式：
echo    python main.py --merge ai_vanvan --ultimate
pause
