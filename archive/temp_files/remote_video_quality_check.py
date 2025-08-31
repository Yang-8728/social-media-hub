#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程视频质量检测工具 - 无需播放视频即可检测质量问题
"""

import os
import subprocess
import json
from pathlib import Path
import sys
sys.path.append('src')

from utils.video_merger import VideoMerger

# 全局FFmpeg路径变量
ffmpeg_path = ""
ffprobe_path = ""

def check_video_quality_remote(video_path):
    """远程检测视频质量"""
    print(f"🔍 检测视频: {video_path}")
    
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在")
        return False
    
    try:
        # 使用ffprobe获取详细信息
        cmd = [
            ffprobe_path, '-v', 'quiet', '-print_format', 'json', 
            '-show_format', '-show_streams', '-show_chapters',
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"❌ FFprobe检测失败: {result.stderr}")
            return False
        
        info = json.loads(result.stdout)
        
        # 分析视频流
        video_streams = [s for s in info['streams'] if s['codec_type'] == 'video']
        audio_streams = [s for s in info['streams'] if s['codec_type'] == 'audio']
        
        print(f"📊 基本信息:")
        print(f"   📄 文件大小: {os.path.getsize(video_path) / (1024*1024):.1f}MB")
        print(f"   ⏱️ 总时长: {float(info['format']['duration']):.1f}秒")
        print(f"   🎥 视频流: {len(video_streams)} 个")
        print(f"   🔊 音频流: {len(audio_streams)} 个")
        
        # 检查视频流质量
        if video_streams:
            v = video_streams[0]
            print(f"\n🎥 视频流分析:")
            print(f"   📐 分辨率: {v.get('width', '?')}x{v.get('height', '?')}")
            print(f"   🎞️ 编码格式: {v.get('codec_name', '?')}")
            print(f"   📊 帧率: {v.get('r_frame_rate', '?')}")
            print(f"   🕐 时长: {float(v.get('duration', 0)):.1f}秒")
            
            # 检查帧率问题
            frame_rate = v.get('r_frame_rate', '0/1')
            if '/' in frame_rate:
                num, den = map(int, frame_rate.split('/'))
                fps = num / den if den > 0 else 0
                if fps > 35:
                    print(f"⚠️ 帧率异常高: {fps:.1f}fps (可能导致加速)")
                elif fps < 20:
                    print(f"⚠️ 帧率异常低: {fps:.1f}fps (可能导致卡顿)")
                else:
                    print(f"✅ 帧率正常: {fps:.1f}fps")
        
        # 检查音频流质量
        if audio_streams:
            a = audio_streams[0]
            print(f"\n🔊 音频流分析:")
            print(f"   🎵 编码格式: {a.get('codec_name', '?')}")
            print(f"   📊 采样率: {a.get('sample_rate', '?')}Hz")
            print(f"   🔈 声道数: {a.get('channels', '?')}")
            print(f"   🕐 时长: {float(a.get('duration', 0)):.1f}秒")
            
            # 检查音视频同步
            if video_streams and audio_streams:
                v_duration = float(video_streams[0].get('duration', 0))
                a_duration = float(audio_streams[0].get('duration', 0))
                sync_diff = abs(v_duration - a_duration)
                
                if sync_diff > 0.1:
                    print(f"⚠️ 音视频时长不匹配: 差异{sync_diff:.2f}秒")
                else:
                    print(f"✅ 音视频时长同步: 差异{sync_diff:.3f}秒")
        
        # 检查时间戳问题
        if 'chapters' in info and info['chapters']:
            print(f"\n📑 章节信息: {len(info['chapters'])} 个")
            
        # 使用ffmpeg检测更多问题
        print(f"\n🔧 深度质量检测:")
        return check_video_issues(video_path)
        
    except Exception as e:
        print(f"❌ 检测异常: {e}")
        return False

def check_video_issues(video_path):
    """检测视频具体问题"""
    issues_found = []
    
    try:
        # 检测冻结帧
        print("   🔍 检测冻结帧...")
        cmd = [
            ffmpeg_path, '-i', video_path, '-vf', 'freezedetect=n=-60dB:d=0.5',
            '-f', 'null', '-', '-v', 'info'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if 'freezedetect' in result.stderr:
            freeze_lines = [line for line in result.stderr.split('\n') if 'freeze_start' in line or 'freeze_end' in line]
            if freeze_lines:
                print(f"   ⚠️ 发现 {len(freeze_lines)//2} 个冻结帧段")
                issues_found.append("冻结帧")
            else:
                print(f"   ✅ 无冻结帧")
        
    except subprocess.TimeoutExpired:
        print("   ⏰ 冻结帧检测超时")
    except Exception as e:
        print(f"   ❌ 冻结帧检测失败: {e}")
    
    try:
        # 检测音频间隙
        print("   🔍 检测音频间隙...")
        cmd = [
            ffmpeg_path, '-i', video_path, '-af', 'silencedetect=noise=-50dB:duration=0.1',
            '-f', 'null', '-', '-v', 'info'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if 'silence_start' in result.stderr:
            silence_lines = [line for line in result.stderr.split('\n') if 'silence_start' in line]
            if len(silence_lines) > 5:  # 超过5个静音段可能有问题
                print(f"   ⚠️ 发现 {len(silence_lines)} 个静音段")
                issues_found.append("音频间隙")
            else:
                print(f"   ✅ 音频连续性正常")
        
    except subprocess.TimeoutExpired:
        print("   ⏰ 音频检测超时")
    except Exception as e:
        print(f"   ❌ 音频检测失败: {e}")
    
    # 返回检测结果
    if issues_found:
        print(f"\n⚠️ 发现的问题: {', '.join(issues_found)}")
        return False
    else:
        print(f"\n✅ 视频质量检测通过")
        return True

def test_merge_and_check():
    """测试合并并检查质量"""
    print("🎬 开始视频合并测试")
    print("=" * 60)
    
    # 使用广告文件夹中的视频进行测试
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if not ads_folder.exists():
        print(f"❌ 广告文件夹不存在: {ads_folder}")
        return
    
    # 获取前5个视频进行快速测试
    video_files = sorted(list(ads_folder.glob("*.mp4")))[:5]
    
    if len(video_files) < 2:
        print(f"❌ 视频文件不足，需要至少2个视频进行测试")
        return
    
    print(f"📁 使用视频文件: {len(video_files)} 个")
    for i, video in enumerate(video_files, 1):
        size_mb = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size_mb:.1f}MB)")
    
    # 初始化合并器
    merger = VideoMerger("ai_vanvan")
    
    # 执行合并
    print(f"\n🔄 开始合并视频...")
    
    try:
        # 准备输出文件
        output_name = f"quality_test_{len(video_files)}videos.mp4"
        output_path = Path("videos/merged/ai_vanvan") / output_name
        
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 执行合并
        success = merger.merge_videos_with_ffmpeg(video_files, str(output_path))
        
        if success:
            print(f"✅ 合并成功: {output_path}")
            
            # 立即进行质量检测
            print(f"\n🔍 开始质量检测...")
            quality_ok = check_video_quality_remote(str(output_path))
            
            if quality_ok:
                print(f"\n🎉 测试结果: 合并质量良好!")
            else:
                print(f"\n⚠️ 测试结果: 发现质量问题，需要进一步优化")
            
            return quality_ok
            
        else:
            print(f"❌ 合并失败")
            return False
            
    except Exception as e:
        print(f"❌ 合并过程异常: {e}")
        return False

def main():
    print("🎥 远程视频质量检测工具")
    print("=" * 40)
    
    # 设置FFmpeg路径
    global ffmpeg_path, ffprobe_path
    ffmpeg_path = r"c:\Code\insDownloader\ffmpeg\ffmpeg.exe"
    ffprobe_path = r"c:\Code\insDownloader\ffmpeg\ffprobe.exe"
    
    # 检查FFmpeg可用性
    try:
        result = subprocess.run([ffmpeg_path, '-version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg可用")
        else:
            print("❌ FFmpeg不可用")
            return
    except:
        print("❌ FFmpeg路径错误或不可用")
        return
    
    # 执行测试
    test_merge_and_check()

if __name__ == "__main__":
    main()
