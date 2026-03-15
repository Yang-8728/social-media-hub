#!/usr/bin/env python3
"""
修复视频跳变问题 - 重新编码视频
"""
import subprocess
import os
import sys

# 获取 ffmpeg 路径
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"✅ 找到 ffmpeg: {FFMPEG}")
except ImportError:
    FFMPEG = 'ffmpeg'
    print("⚠️ 使用系统 ffmpeg")

input_file = r"C:\Users\USER\Videos\剪映剪辑的\11月12日.mp4"
output_file = r"C:\Users\USER\Videos\剪映剪辑的\11月12日_fixed.mp4"
backup_file = r"C:\Users\USER\Videos\剪映剪辑的\11月12日_backup.mp4"

print(f"🔍 检查文件: {input_file}")
if not os.path.exists(input_file):
    print(f"❌ 文件不存在!")
    sys.exit(1)

file_size = os.path.getsize(input_file) / (1024*1024)
print(f"📦 文件大小: {file_size:.2f} MB")

# 检查视频是否有错误
print("\n🔍 检查视频错误...")
check_cmd = [
    FFMPEG, '-v', 'error', '-i', input_file,
    '-f', 'null', '-'
]

try:
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    if result.stderr:
        print(f"⚠️ 发现错误:\n{result.stderr[:500]}")
    else:
        print("✅ 未发现明显错误")
except FileNotFoundError:
    print("❌ ffmpeg 未安装或不在 PATH 中")
    print("尝试使用本地 ffmpeg...")
    # 你可能需要指定 ffmpeg 的完整路径

print("\n🔧 开始修复视频(重新编码)...")

# 修复方案: 重新编码,使用更兼容的参数
fix_cmd = [
    FFMPEG, '-i', input_file,
    '-c:v', 'libx264',           # 使用 H.264 编码
    '-preset', 'medium',          # 编码速度/质量平衡
    '-crf', '23',                 # 质量参数(18-28,越小越好)
    '-c:a', 'aac',                # 音频编码
    '-b:a', '128k',               # 音频比特率
    '-movflags', '+faststart',    # Web 优化
    '-y',                         # 覆盖输出文件
    output_file
]

print(f"📝 命令: {' '.join(fix_cmd)}")

try:
    result = subprocess.run(fix_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\n✅ 修复完成!")
        print(f"📦 新文件: {output_file}")
        
        new_size = os.path.getsize(output_file) / (1024*1024)
        print(f"📦 新文件大小: {new_size:.2f} MB")
        
        # 备份原文件
        print(f"\n💾 备份原文件到: {backup_file}")
        os.rename(input_file, backup_file)
        
        # 重命名新文件
        print(f"📝 重命名修复文件为原文件名")
        os.rename(output_file, input_file)
        
        print("\n✅ 完成! 原文件已备份,修复后的文件已替换")
        print(f"   原文件(备份): {backup_file}")
        print(f"   修复文件: {input_file}")
        
    else:
        print(f"\n❌ 修复失败!")
        print(f"错误信息:\n{result.stderr}")
        
except FileNotFoundError:
    print("\n❌ 找不到 ffmpeg 命令")
    print("请安装 ffmpeg 或将其添加到 PATH")
    print("或者指定 ffmpeg 的完整路径")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")
