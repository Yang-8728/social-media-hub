import os
import shutil
import glob
from datetime import datetime

# 最后成功上传日期：2025-10-28
CUTOFF_DATE = "2025-10-28"
cutoff = datetime.strptime(CUTOFF_DATE, "%Y-%m-%d").date()

print("=" * 70)
print(f"🧹 清理从 {CUTOFF_DATE} 开始的所有下载数据")
print("=" * 70)

# 1. 清理下载目录中的日期文件夹
print("\n📁 第1步：清理下载目录中的日期文件夹...")
download_paths = glob.glob('videos/downloads/**/*', recursive=True)
deleted_folders = []
deleted_files = []

for path in download_paths:
    if not os.path.exists(path):
        continue
        
    # 提取日期部分（文件名或文件夹名中的日期）
    basename = os.path.basename(path)
    
    # 匹配 2025-10-XX 格式
    if basename.startswith('2025-'):
        try:
            # 提取日期部分
            date_part = basename[:10]  # 2025-10-28
            if len(date_part) == 10 and date_part[4] == '-' and date_part[7] == '-':
                file_date = datetime.strptime(date_part, "%Y-%m-%d").date()
                
                # 如果是10-28或之后的
                if file_date >= cutoff:
                    if os.path.isdir(path):
                        print(f"  删除文件夹: {path}")
                        shutil.rmtree(path)
                        deleted_folders.append(path)
                    elif os.path.isfile(path):
                        # 检查文件的修改时间
                        mtime = datetime.fromtimestamp(os.path.getmtime(path)).date()
                        if mtime >= cutoff:
                            print(f"  删除文件: {path}")
                            os.remove(path)
                            deleted_files.append(path)
        except:
            pass

print(f"✅ 删除了 {len(deleted_folders)} 个文件夹")
print(f"✅ 删除了 {len(deleted_files)} 个文件")

# 2. 清理日志文件
print("\n📝 第2步：清理应用日志...")
log_files = glob.glob('logs/app/2025-10-*.log')
deleted_logs = []

for log_file in log_files:
    basename = os.path.basename(log_file)
    # 提取日期 2025-10-28
    date_part = basename[:10]
    try:
        log_date = datetime.strptime(date_part, "%Y-%m-%d").date()
        if log_date >= cutoff:
            print(f"  删除日志: {log_file}")
            os.remove(log_file)
            deleted_logs.append(log_file)
    except:
        pass

print(f"✅ 删除了 {len(deleted_logs)} 个日志文件")

# 3. 清理其他日志目录
print("\n📋 第3步：检查其他日志目录...")
log_dirs = ['logs/cache', 'logs/downloads', 'logs/episodes', 'logs/merges']
for log_dir in log_dirs:
    if os.path.exists(log_dir):
        files = glob.glob(f'{log_dir}/2025-10-*.log')
        for f in files:
            basename = os.path.basename(f)
            date_part = basename[:10]
            try:
                file_date = datetime.strptime(date_part, "%Y-%m-%d").date()
                if file_date >= cutoff:
                    print(f"  删除: {f}")
                    os.remove(f)
            except:
                pass

# 4. 统计还剩多少视频
print("\n📊 第4步：统计剩余视频...")
remaining_videos = glob.glob('videos/downloads/**/*.mp4', recursive=True)
print(f"✅ 剩余视频总数: {len(remaining_videos)} 个")

print("\n" + "=" * 70)
print("🎉 清理完成！")
print("=" * 70)
print("\n提示：")
print("  - 已删除 2025-10-28 及之后的所有下载文件夹")
print("  - 已删除相关日志文件")
print("  - 现在可以重新下载这些日期的视频")
print("=" * 70)
