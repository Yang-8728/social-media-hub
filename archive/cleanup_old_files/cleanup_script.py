# 清理根目录不必要的Python文件

import os
import shutil

# 要清理的文件列表
cleanup_files = [
    # 临时文件
    'download_retry_explanation.py',
    'final_merge_preparation.py',
    'find_files.py',
    'integrity_report.py',
    'match_records_files.py',
    'merge_logs.py',
    'quick_test.py',
    'recover_records.py',
    'search_files.py',
    
    # 调试工具
    'debug_download_logic.py',
    'debug_paths.py',
    'debug_unicode.py',
    
    # 分析工具
    'analyze_download_failures.py',
    'analyze_merge_behavior.py',
    'analyze_records.py',
    'analyze_videos.py',
    
    # 检查工具  
    'check_downloads.py',
    'check_exact_merge_count.py',
    'check_file_integrity.py',
    'check_mergeable_videos.py',
    'check_status.py',
    'check_videos.py',
    
    # 其他工具
    'fix_and_analyze.py'
]

# 要移动到tests的文件
move_to_tests = [
    'test_login.py',
    'test_merge.py', 
    'test_prescan.py',
    'test_record.py'
]

print("=== 清理根目录不必要的文件 ===")

# 1. 移动文件到备份文件夹
backup_folder = 'cleanup_old_files'
moved_count = 0

for file in cleanup_files:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join(backup_folder, file))
            print(f"✅ 移动到备份: {file}")
            moved_count += 1
        except Exception as e:
            print(f"❌ 移动失败: {file} - {e}")

# 2. 移动测试文件到tests目录
tests_moved = 0
for file in move_to_tests:
    if os.path.exists(file):
        try:
            shutil.move(file, os.path.join('tests', file))
            print(f"✅ 移动到tests: {file}")
            tests_moved += 1
        except Exception as e:
            print(f"❌ 移动失败: {file} - {e}")

# 3. 清理这个分析脚本本身
if os.path.exists('analyze_root_files.py'):
    shutil.move('analyze_root_files.py', os.path.join(backup_folder, 'analyze_root_files.py'))
    moved_count += 1

print()
print(f"📊 清理完成:")
print(f"  - 备份文件: {moved_count} 个")
print(f"  - 移动到tests: {tests_moved} 个")
print()
print("现在根目录应该只剩下:")
print("  - main.py (核心入口)")
print("  - fix_unicode_paths.py (重要修复工具)")
print("  - 其他非.py文件和目录")
