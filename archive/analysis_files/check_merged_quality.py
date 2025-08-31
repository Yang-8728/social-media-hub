#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接检查已合并视频的质量问题
使用Windows自带工具检查音频、视频信息
"""

import os
import subprocess
from pathlib import Path

def check_merged_video_issues(video_path):
    """检查单个合并视频的常见问题"""
    print(f"\n🔍 检查视频: {os.path.basename(video_path)}")
    print("=" * 60)
    
    # 文件基本信息
    stat = os.stat(video_path)
    size_mb = stat.st_size / (1024 * 1024)
    print(f"📦 文件大小: {size_mb:.1f}MB")
    
    # 尝试使用PowerShell检查视频属性
    try:
        # 使用PowerShell获取媒体信息
        ps_cmd = f'''
$file = Get-Item "{video_path}"
$shell = New-Object -ComObject Shell.Application
$folder = $shell.NameSpace($file.Directory.FullName)
$item = $folder.ParseName($file.Name)

# 获取视频长度 (属性27)
$duration = $folder.GetDetailsOf($item, 27)
if ($duration) {{ 
    Write-Host "⏱️  视频时长: $duration"
}} else {{
    Write-Host "⚠️  无法获取视频时长"
}}

# 获取视频尺寸 (属性31)  
$dimensions = $folder.GetDetailsOf($item, 31)
if ($dimensions) {{
    Write-Host "📐 视频尺寸: $dimensions"
}} else {{
    Write-Host "⚠️  无法获取视频尺寸"
}}

# 获取比特率 (属性28)
$bitrate = $folder.GetDetailsOf($item, 28)  
if ($bitrate) {{
    Write-Host "📊 比特率: $bitrate"
}} else {{
    Write-Host "⚠️  无法获取比特率信息"
}}
'''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True, text=True, encoding='utf-8'
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print(result.stdout.strip())
        else:
            print("⚠️  PowerShell检查失败，使用基本检查")
            
    except Exception as e:
        print(f"⚠️  PowerShell检查出错: {e}")
    
    # 文件头检查
    try:
        with open(video_path, 'rb') as f:
            header = f.read(32)
            
            # 检查MP4文件头
            if b'ftyp' in header[:12]:
                print("✅ MP4文件头正常")
                
                # 检查是否包含音频相关标识
                f.seek(0)
                chunk = f.read(8192)  # 读取更多数据
                
                audio_indicators = [b'mp4a', b'aac ', b'soun']
                has_audio_sign = any(indicator in chunk for indicator in audio_indicators)
                
                if has_audio_sign:
                    print("✅ 检测到音频轨道标识")
                else:
                    print("⚠️  未检测到明显的音频标识")
                    
                # 检查视频编码标识
                video_indicators = [b'avc1', b'h264', b'vide']
                has_video_sign = any(indicator in chunk for indicator in video_indicators)
                
                if has_video_sign:
                    print("✅ 检测到H.264视频编码")
                else:
                    print("⚠️  视频编码标识不明确")
                    
            else:
                print("❌ 文件头异常，可能文件损坏")
                
    except Exception as e:
        print(f"❌ 文件检查失败: {e}")
    
    # 基于文件大小和名称的启发式检查
    filename = os.path.basename(video_path)
    
    # 提取视频数量
    if 'merged' in filename and 'videos' in filename:
        import re
        match = re.search(r'(\d+)videos', filename)
        if match:
            video_count = int(match.group(1))
            avg_size = size_mb / video_count
            
            print(f"🔢 合并了 {video_count} 个视频")
            print(f"📊 平均每个原视频: {avg_size:.1f}MB")
            
            # 经验判断
            if avg_size < 0.8:
                print("⚠️  原视频可能较短或质量偏低")
            elif avg_size > 4:
                print("✅ 原视频质量应该较好")
            else:
                print("📋 原视频大小适中")
    
    # 播放建议
    print("\n🎯 建议检查项目:")
    print("1. 用Windows媒体播放器或VLC播放视频")
    print("2. 检查是否有声音输出")
    print("3. 观察是否有卡顿或跳帧")
    print("4. 确认画质是否清晰")

def main():
    """主函数"""
    print("🔍 检查已合并视频质量问题")
    print("=" * 50)
    
    # 合并视频目录
    merged_dir = Path("videos/merged/ai_vanvan")
    
    if not merged_dir.exists():
        print("❌ 合并视频目录不存在")
        return
    
    # 获取所有合并视频
    video_files = list(merged_dir.glob("*.mp4"))
    
    if not video_files:
        print("❌ 未找到合并视频")
        return
    
    print(f"📁 找到 {len(video_files)} 个合并视频")
    
    # 逐个检查
    for video_file in video_files:
        check_merged_video_issues(str(video_file))
    
    print("\n" + "=" * 50)
    print("📋 常见问题及解决方案:")
    print()
    print("🔇 如果没有声音:")
    print("   原因: FFmpeg -c copy模式音频流映射问题") 
    print("   解决: 重新合并时使用 -c:a aac 重编码音频")
    print()
    print("🎬 如果有跳帧:")
    print("   原因: 源视频帧率不一致或时间戳问题")
    print("   解决: 重新合并时使用 -r 30 统一帧率")
    print()
    print("🎭 如果音视频不同步:")
    print("   原因: 编码时时间戳处理问题")
    print("   解决: 重新合并时添加 -async 1 参数")
    print()
    print("💡 如果发现问题，建议使用改进的合并参数重新处理")

if __name__ == "__main__":
    main()
