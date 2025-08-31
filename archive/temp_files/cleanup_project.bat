@echo off
echo 🧹 开始清理项目根目录...

REM 创建归档目录
if not exist "archive" mkdir archive
if not exist "archive\test_files" mkdir archive\test_files
if not exist "archive\debug_files" mkdir archive\debug_files
if not exist "archive\analysis_files" mkdir archive\analysis_files
if not exist "archive\temp_files" mkdir archive\temp_files

echo 📦 移动测试文件...
move test_*.py archive\test_files\ 2>nul

echo 🔍 移动调试文件...
move debug_*.py archive\debug_files\ 2>nul

echo 📊 移动分析文件...
move analyze_*.py archive\analysis_files\ 2>nul
move check_*.py archive\analysis_files\ 2>nul
move diagnose_*.py archive\analysis_files\ 2>nul

echo 🗂️ 移动临时文件...
move *_fix.py archive\temp_files\ 2>nul
move *_test.py archive\temp_files\ 2>nul
move fix_*.py archive\temp_files\ 2>nul
move final_*.py archive\temp_files\ 2>nul
move quick_*.py archive\temp_files\ 2>nul
move simple_*.py archive\temp_files\ 2>nul
move smart_*.py archive\temp_files\ 2>nul
move advanced_*.py archive\temp_files\ 2>nul
move auto_*.py archive\temp_files\ 2>nul
move copy_*.py archive\temp_files\ 2>nul
move find_*.py archive\temp_files\ 2>nul
move mark_*.py archive\temp_files\ 2>nul
move match_*.py archive\temp_files\ 2>nul
move merge_*.py archive\temp_files\ 2>nul
move optimization_*.py archive\temp_files\ 2>nul
move organize_*.py archive\temp_files\ 2>nul
move original_*.py archive\temp_files\ 2>nul
move parse_*.py archive\temp_files\ 2>nul
move quality_*.py archive\temp_files\ 2>nul
move recover_*.py archive\temp_files\ 2>nul
move remerge_*.py archive\temp_files\ 2>nul
move remote_*.py archive\temp_files\ 2>nul
move search_*.py archive\temp_files\ 2>nul
move sync_*.py archive\temp_files\ 2>nul
move ultimate_*.py archive\temp_files\ 2>nul
move upload.py archive\temp_files\ 2>nul
move upload_*.py archive\temp_files\ 2>nul
move video_*.py archive\temp_files\ 2>nul
move working_*.py archive\temp_files\ 2>nul
move clean_*.py archive\temp_files\ 2>nul
move cleanup_*.py archive\temp_files\ 2>nul
move integrity_*.py archive\temp_files\ 2>nul
move download_*.py archive\temp_files\ 2>nul

echo 📄 移动临时文档...
move *.txt archive\temp_files\ 2>nul
move setup_*.bat archive\temp_files\ 2>nul

echo ✅ 清理完成！
echo 📁 已归档文件到 archive 文件夹
echo 🎯 保留的核心文件:
echo    - main.py (主程序)
echo    - requirements.txt (依赖)
echo    - README.md (说明文档)
echo    - LICENSE (许可证)
echo    - CHANGELOG.md (更新日志)
echo    - RELEASE_NOTES_v2.0.0.md (发布说明)
echo    - create_tag_v2.bat (标签创建脚本)
echo    - view-log.bat (日志查看脚本)

pause
