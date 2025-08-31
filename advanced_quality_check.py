#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级视频质量检测工具 - 使用文本分析方法
"""

import os
import subprocess
from pathlib import Path
import json
import sys
sys.path.append('src')

def get_ffprobe_path():
    """尝试找到可用的ffprobe路径"""
    possible_paths = [
        "ffmpeg",  # 如果ffmpeg文件同时包含ffprobe
        "ffprobe",
        "ffprobe.exe",
        r"C:\ffmpeg\bin\ffprobe.exe",
        r"C:\Program Files\ffmpeg\bin\ffprobe.exe",
    ]
    
    for path in possible_paths:
        try:
            result = subprocess.run([path, "-version"], 
                                 capture_output=True, 
                                 text=True, 
                                 timeout=5)
            if result.returncode == 0:
                print(f"✅ 找到ffprobe: {path}")
                return path
        except:
            continue
    
    return None

def analyze_video_metadata(video_path, ffprobe_path):
    """使用ffprobe分析视频元数据"""
    try:
        # 获取基本信息
        cmd = [
            ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return None
        
        return json.loads(result.stdout)
    
    except Exception as e:
        print(f"❌ 元数据分析失败: {e}")
        return None

def check_video_basic_info(metadata):
    """检查视频基本信息"""
    if not metadata:
        return {}
    
    info = {}
    
    # 查找视频流
    video_stream = None
    audio_stream = None
    
    for stream in metadata.get('streams', []):
        if stream.get('codec_type') == 'video':
            video_stream = stream
        elif stream.get('codec_type') == 'audio':
            audio_stream = stream
    
    # 视频信息
    if video_stream:
        info['video_codec'] = video_stream.get('codec_name', 'unknown')
        info['resolution'] = f"{video_stream.get('width', '?')}x{video_stream.get('height', '?')}"
        info['fps'] = video_stream.get('r_frame_rate', 'unknown')
        info['duration'] = float(video_stream.get('duration', 0))
    
    # 音频信息
    if audio_stream:
        info['audio_codec'] = audio_stream.get('codec_name', 'unknown')
        info['sample_rate'] = audio_stream.get('sample_rate', 'unknown')
        info['channels'] = audio_stream.get('channels', 'unknown')
    
    # 总体信息
    format_info = metadata.get('format', {})
    info['format'] = format_info.get('format_name', 'unknown')
    info['total_duration'] = float(format_info.get('duration', 0))
    
    return info

def simple_quality_check(video_path):
    """简单的视频质量检查（不需要ffprobe）"""
    print(f"\n🔍 检查文件: {video_path.name}")
    
    checks = {}
    
    # 1. 文件大小检查
    size_mb = video_path.stat().st_size / (1024*1024)
    checks['file_size'] = f"{size_mb:.1f}MB"
    
    if size_mb < 0.1:
        checks['size_warning'] = "⚠️ 文件过小，可能损坏"
    elif size_mb > 500:
        checks['size_warning'] = "⚠️ 文件很大，可能有质量问题"
    else:
        checks['size_ok'] = "✅ 文件大小正常"
    
    # 2. 文件头检查
    try:
        with open(video_path, 'rb') as f:
            header = f.read(100)
            
            # 检查MP4文件头
            if b'ftyp' in header:
                checks['format'] = "✅ MP4格式正常"
            elif b'RIFF' in header:
                checks['format'] = "✅ AVI格式"
            elif b'FLV' in header:
                checks['format'] = "✅ FLV格式"
            else:
                checks['format'] = "⚠️ 文件格式可能有问题"
    
    except Exception as e:
        checks['format'] = f"❌ 文件读取失败: {e}"
    
    # 3. 文件完整性检查
    try:
        with open(video_path, 'rb') as f:
            f.seek(-100, 2)  # 读取文件末尾
            footer = f.read(100)
            checks['integrity'] = "✅ 文件读取完整"
    except Exception as e:
        checks['integrity'] = f"⚠️ 文件可能不完整: {e}"
    
    return checks

def advanced_quality_check(video_path, ffprobe_path):
    """高级质量检查（需要ffprobe）"""
    print(f"\n🔬 高级检查: {video_path.name}")
    
    # 获取元数据
    metadata = analyze_video_metadata(video_path, ffprobe_path)
    if not metadata:
        return {"error": "无法获取视频元数据"}
    
    info = check_video_basic_info(metadata)
    checks = {}
    
    # 视频检查
    if 'video_codec' in info:
        checks['video_codec'] = f"视频编码: {info['video_codec']}"
        checks['resolution'] = f"分辨率: {info['resolution']}"
        checks['fps'] = f"帧率: {info['fps']}"
        
        # 检查常见问题
        if info['video_codec'] in ['h264', 'h265', 'vp9']:
            checks['codec_ok'] = "✅ 视频编码格式良好"
        else:
            checks['codec_warning'] = f"⚠️ 视频编码可能不兼容: {info['video_codec']}"
    
    # 音频检查
    if 'audio_codec' in info:
        checks['audio_codec'] = f"音频编码: {info['audio_codec']}"
        checks['sample_rate'] = f"采样率: {info['sample_rate']}"
        checks['channels'] = f"声道: {info['channels']}"
        
        if info['audio_codec'] in ['aac', 'mp3', 'opus']:
            checks['audio_ok'] = "✅ 音频编码格式良好"
        else:
            checks['audio_warning'] = f"⚠️ 音频编码可能不兼容: {info['audio_codec']}"
    
    # 时长检查
    if 'duration' in info and 'total_duration' in info:
        duration_diff = abs(info['duration'] - info['total_duration'])
        if duration_diff < 0.1:
            checks['duration_ok'] = "✅ 音视频时长一致"
        else:
            checks['duration_warning'] = f"⚠️ 音视频时长不一致 (差异: {duration_diff:.2f}秒)"
    
    return checks

def test_merged_video_quality():
    """测试合并视频的质量"""
    print("🎬 合并视频质量检测")
    print("=" * 50)
    
    # 查找最新的测试合并文件
    merged_folder = Path("videos/merged/ai_vanvan")
    test_file = merged_folder / "quality_test_3videos.mp4"
    
    if not test_file.exists():
        print(f"❌ 测试文件不存在: {test_file}")
        return
    
    print(f"📁 检测文件: {test_file.name}")
    
    # 基本检查（总是可用）
    basic_checks = simple_quality_check(test_file)
    print(f"\n📊 基本检查结果:")
    for key, value in basic_checks.items():
        print(f"   {value}")
    
    # 尝试高级检查
    ffprobe_path = get_ffprobe_path()
    if ffprobe_path:
        advanced_checks = advanced_quality_check(test_file, ffprobe_path)
        print(f"\n🔬 高级检查结果:")
        for key, value in advanced_checks.items():
            if not key.endswith('_ok') and not key.endswith('_warning'):
                print(f"   {value}")
        
        # 显示问题和成功项
        warnings = [v for k, v in advanced_checks.items() if k.endswith('_warning')]
        successes = [v for k, v in advanced_checks.items() if k.endswith('_ok')]
        
        if successes:
            print(f"\n✅ 检查通过:")
            for success in successes:
                print(f"   {success}")
        
        if warnings:
            print(f"\n⚠️ 发现问题:")
            for warning in warnings:
                print(f"   {warning}")
        
        if not warnings:
            print(f"\n🎉 视频质量检查全部通过!")
    else:
        print(f"\n💡 提示: 未找到ffprobe，只能进行基本检查")
        print(f"   如需详细分析，请安装FFmpeg工具包")

def compare_with_source():
    """与源文件进行对比"""
    print(f"\n📊 源文件对比分析")
    print("=" * 40)
    
    # 源文件夹
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    source_files = sorted(list(ads_folder.glob("*.mp4")))[:3]
    
    # 合并文件
    merged_file = Path("videos/merged/ai_vanvan/quality_test_3videos.mp4")
    
    if not merged_file.exists():
        print(f"❌ 合并文件不存在")
        return
    
    print(f"🔍 对比 {len(source_files)} 个源文件和1个合并文件:")
    
    # 计算大小对比
    total_source_size = sum(f.stat().st_size for f in source_files)
    merged_size = merged_file.stat().st_size
    
    total_source_mb = total_source_size / (1024*1024)
    merged_mb = merged_size / (1024*1024)
    
    print(f"📦 源文件总大小: {total_source_mb:.1f}MB")
    print(f"📦 合并文件大小: {merged_mb:.1f}MB")
    
    size_ratio = merged_mb / total_source_mb
    print(f"📈 大小比率: {size_ratio:.3f}")
    
    if 0.95 <= size_ratio <= 1.05:
        print(f"✅ 大小比率理想 (损失极小)")
    elif 0.8 <= size_ratio < 0.95:
        print(f"✅ 大小比率良好 (轻微压缩)")
    elif 0.6 <= size_ratio < 0.8:
        print(f"⚠️ 大小比率偏低 (可能质量损失)")
    elif size_ratio < 0.6:
        print(f"❌ 大小比率过低 (严重质量损失)")
    elif size_ratio > 1.1:
        print(f"⚠️ 大小比率过高 (可能重复数据)")
    
    # 检查是否为简单拼接
    if 0.98 <= size_ratio <= 1.02:
        print(f"💡 推测: 使用了流复制模式 (-c copy)，质量无损")
    elif size_ratio < 0.9:
        print(f"💡 推测: 可能进行了重新编码，有质量损失")

def main():
    print("🎥 高级视频质量检测工具")
    print("=" * 50)
    
    # 测试合并视频质量
    test_merged_video_quality()
    
    # 与源文件对比
    compare_with_source()
    
    print(f"\n📋 总结:")
    print(f"✅ 质量检测完成")
    print(f"💡 建议: 如果所有检查都通过，说明合并功能正常工作")
    print(f"💡 提示: 如果发现问题，可以调整FFmpeg参数重新合并")

if __name__ == "__main__":
    main()
