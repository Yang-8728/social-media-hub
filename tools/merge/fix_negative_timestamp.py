#!/usr/bin/env python3
"""
修复负数时间戳的问题视频
"""
import os
import subprocess

def fix_negative_timestamp_video(input_path, output_path):
    """修复具有负数时间戳的视频"""
    try:
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        
        # 使用特殊参数修复时间戳问题
        cmd = [
            ffmpeg_exe,
            "-i", input_path,
            "-avoid_negative_ts", "make_zero",  # 将负时间戳设为0
            "-c:v", "libx264",                  # 重新编码视频
            "-crf", "23",
            "-preset", "medium",
            "-c:a", "aac",                      # 重新编码音频
            "-b:a", "128k",                     # 提升音频比特率
            "-ar", "44100",
            "-fflags", "+genpts",               # 重新生成时间戳
            "-y",
            output_path
        ]
        
        print(f"🔧 修复负数时间戳: {os.path.basename(input_path)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 时间戳修复成功")
            return True
        else:
            print(f"❌ 修复失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 修复出错: {e}")
        return False

def verify_fixed_video(video_path):
    """验证修复后的视频时间戳"""
    try:
        ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        cmd = [
            ffprobe_exe,
            "-v", "quiet",
            "-select_streams", "v:0",
            "-show_entries", "packet=pts_time,dts_time",
            "-of", "csv=p=0",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')[:5]  # 只看前5个包
        
        print(f"🔍 验证修复后的时间戳:")
        has_negative = False
        
        for i, line in enumerate(lines):
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 2:
                    pts = parts[0] if parts[0] != 'N/A' else '无'
                    dts = parts[1] if parts[1] != 'N/A' else '无'
                    
                    # 检查是否还有负数
                    if dts != '无' and float(dts) < 0:
                        has_negative = True
                    
                    print(f"  包{i+1}: PTS={pts}, DTS={dts}")
        
        if has_negative:
            print("❌ 仍然存在负数时间戳")
            return False
        else:
            print("✅ 时间戳修复成功，无负数")
            return True
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    problem_video = "2025-06-11_18-34-31_UTC.mp4"
    input_path = os.path.join("videos", "downloads", "ai_vanvan", "2025-09-01", problem_video)
    output_path = f"fixed_{problem_video}"
    
    print("🎯 修复负数时间戳视频")
    print("=" * 50)
    
    if not os.path.exists(input_path):
        print(f"❌ 原始文件不存在: {input_path}")
        return
    
    # 修复视频
    if fix_negative_timestamp_video(input_path, output_path):
        # 验证修复效果
        if verify_fixed_video(output_path):
            # 检查文件大小
            original_size = os.path.getsize(input_path) / (1024*1024)
            fixed_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"\n📊 修复结果:")
            print(f"  原始文件: {original_size:.1f}MB")
            print(f"  修复文件: {fixed_size:.1f}MB")
            print(f"  输出文件: {output_path}")
            
            print(f"\n💡 建议:")
            print(f"  1. 用修复后的文件替换原始文件")
            print(f"  2. 重新运行合并脚本")
            print(f"  3. 测试1:39位置是否解决")
        else:
            print(f"\n❌ 修复验证失败")
    else:
        print(f"\n❌ 修复过程失败")
        print(f"\n💡 备选方案:")
        print(f"  完全排除这个视频文件")

if __name__ == "__main__":
    main()
