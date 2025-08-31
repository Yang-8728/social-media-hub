#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程视频质量检测工具 - 无需播放即可检测音视频同步和质量问题
"""

import os
import subprocess
import json
from pathlib import Path
import re

def run_ffprobe(video_path, *args):
    """运行ffprobe命令"""
    cmd = ["ffmpeg/ffprobe.exe", "-v", "quiet"] + list(args) + [str(video_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", str(e)

def analyze_video_technical_info(video_path):
    """分析视频技术信息"""
    print(f"🔍 分析视频: {Path(video_path).name}")
    print("-" * 50)
    
    # 1. 基本信息
    stdout, stderr = run_ffprobe(video_path, "-show_format", "-show_streams", "-of", "json")
    
    if stdout:
        try:
            data = json.loads(stdout)
            
            # 格式信息
            format_info = data.get('format', {})
            duration = float(format_info.get('duration', 0))
            size = int(format_info.get('size', 0))
            bitrate = int(format_info.get('bit_rate', 0))
            
            print(f"📊 基本信息:")
            print(f"   ⏱️ 时长: {duration:.2f}秒 ({duration//60:.0f}分{duration%60:.0f}秒)")
            print(f"   💾 大小: {size/1024/1024:.1f}MB")
            print(f"   📡 码率: {bitrate//1000}kbps")
            
            # 流信息
            video_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'video']
            audio_streams = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
            
            print(f"\n🎥 视频流信息:")
            for i, stream in enumerate(video_streams):
                width = stream.get('width', 0)
                height = stream.get('height', 0)
                fps = stream.get('r_frame_rate', '0/1')
                codec = stream.get('codec_name', '未知')
                
                # 计算实际帧率
                if '/' in fps:
                    num, den = map(int, fps.split('/'))
                    actual_fps = num / den if den != 0 else 0
                else:
                    actual_fps = float(fps)
                
                print(f"   📺 流{i+1}: {width}x{height} @ {actual_fps:.2f}fps ({codec})")
            
            print(f"\n🔊 音频流信息:")
            for i, stream in enumerate(audio_streams):
                codec = stream.get('codec_name', '未知')
                sample_rate = stream.get('sample_rate', '未知')
                channels = stream.get('channels', '未知')
                
                print(f"   🎵 流{i+1}: {codec}, {sample_rate}Hz, {channels}声道")
            
            return {
                'duration': duration,
                'size': size,
                'video_streams': len(video_streams),
                'audio_streams': len(audio_streams),
                'has_issues': False
            }
            
        except json.JSONDecodeError as e:
            print(f"❌ 解析JSON失败: {e}")
            return {'has_issues': True, 'error': str(e)}
    else:
        print(f"❌ ffprobe执行失败: {stderr}")
        return {'has_issues': True, 'error': stderr}

def check_audio_video_sync(video_path):
    """检查音视频同步问题"""
    print(f"\n🔄 检查音视频同步...")
    
    # 检查音视频时长差异
    stdout, stderr = run_ffprobe(video_path, "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0")
    video_duration = float(stdout) if stdout and stdout.replace('.', '').isdigit() else 0
    
    stdout, stderr = run_ffprobe(video_path, "-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "csv=p=0")
    audio_duration = float(stdout) if stdout and stdout.replace('.', '').isdigit() else 0
    
    if video_duration > 0 and audio_duration > 0:
        sync_diff = abs(video_duration - audio_duration)
        print(f"   🎥 视频时长: {video_duration:.3f}秒")
        print(f"   🔊 音频时长: {audio_duration:.3f}秒")
        print(f"   ⚖️ 同步差异: {sync_diff:.3f}秒")
        
        if sync_diff > 0.1:
            print(f"   ⚠️ 警告: 音视频时长差异较大 ({sync_diff:.3f}秒)")
            return {'sync_issue': True, 'sync_diff': sync_diff}
        else:
            print(f"   ✅ 音视频同步良好")
            return {'sync_issue': False, 'sync_diff': sync_diff}
    else:
        print(f"   ❌ 无法获取音视频时长")
        return {'sync_issue': True, 'error': '无法获取时长'}

def detect_frame_issues(video_path):
    """检测帧率和画面问题"""
    print(f"\n🖼️ 检测帧率和画面问题...")
    
    # 检查帧率一致性
    stdout, stderr = run_ffprobe(video_path, "-select_streams", "v:0", "-show_entries", "packet=pts_time", "-of", "csv=p=0")
    
    if stdout:
        timestamps = []
        for line in stdout.strip().split('\n')[:100]:  # 只检查前100帧
            try:
                ts = float(line.strip())
                timestamps.append(ts)
            except:
                continue
        
        if len(timestamps) >= 10:
            # 计算帧间隔
            intervals = []
            for i in range(1, len(timestamps)):
                interval = timestamps[i] - timestamps[i-1]
                if interval > 0:
                    intervals.append(interval)
            
            if intervals:
                avg_interval = sum(intervals) / len(intervals)
                max_interval = max(intervals)
                min_interval = min(intervals)
                
                expected_fps = 1.0 / avg_interval if avg_interval > 0 else 0
                
                print(f"   📊 帧率分析:")
                print(f"   ⚡ 平均帧间隔: {avg_interval:.4f}秒")
                print(f"   🎯 推算帧率: {expected_fps:.2f}fps")
                print(f"   📈 最大间隔: {max_interval:.4f}秒")
                print(f"   📉 最小间隔: {min_interval:.4f}秒")
                
                # 检查帧率稳定性
                interval_variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
                
                if interval_variance > 0.001:
                    print(f"   ⚠️ 警告: 帧率不稳定，方差={interval_variance:.6f}")
                    return {'frame_issue': True, 'variance': interval_variance}
                else:
                    print(f"   ✅ 帧率稳定")
                    return {'frame_issue': False, 'variance': interval_variance}
    
    print(f"   ❌ 无法分析帧率")
    return {'frame_issue': True, 'error': '无法获取帧时间戳'}

def check_audio_continuity(video_path):
    """检查音频连续性"""
    print(f"\n🎵 检查音频连续性...")
    
    # 获取音频包时间戳
    stdout, stderr = run_ffprobe(video_path, "-select_streams", "a:0", "-show_entries", "packet=pts_time", "-of", "csv=p=0")
    
    if stdout:
        audio_timestamps = []
        for line in stdout.strip().split('\n')[:200]:  # 检查前200个音频包
            try:
                ts = float(line.strip())
                audio_timestamps.append(ts)
            except:
                continue
        
        if len(audio_timestamps) >= 10:
            # 检查音频包间隔
            gaps = []
            for i in range(1, len(audio_timestamps)):
                gap = audio_timestamps[i] - audio_timestamps[i-1]
                if gap > 0:
                    gaps.append(gap)
            
            if gaps:
                avg_gap = sum(gaps) / len(gaps)
                max_gap = max(gaps)
                
                print(f"   📊 音频包分析:")
                print(f"   ⚡ 平均间隔: {avg_gap:.4f}秒")
                print(f"   📈 最大间隔: {max_gap:.4f}秒")
                
                # 检查是否有异常大的间隔（可能表示音频中断）
                large_gaps = [g for g in gaps if g > avg_gap * 3]
                
                if large_gaps:
                    print(f"   ⚠️ 发现 {len(large_gaps)} 个异常间隔，可能有音频中断")
                    return {'audio_issue': True, 'large_gaps': len(large_gaps)}
                else:
                    print(f"   ✅ 音频连续性良好")
                    return {'audio_issue': False, 'large_gaps': 0}
    
    print(f"   ❌ 无法分析音频连续性")
    return {'audio_issue': True, 'error': '无法获取音频时间戳'}

def check_encoding_errors(video_path):
    """检查编码错误"""
    print(f"\n🔧 检查编码错误...")
    
    # 使用ffmpeg验证文件完整性
    cmd = ["ffmpeg/ffmpeg.exe", "-v", "error", "-i", str(video_path), "-f", "null", "-"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        stderr = result.stderr.strip()
        
        if stderr:
            error_lines = stderr.split('\n')
            serious_errors = [line for line in error_lines if any(keyword in line.lower() for keyword in ['error', 'corrupt', 'invalid', 'broken'])]
            
            if serious_errors:
                print(f"   ❌ 发现编码错误:")
                for error in serious_errors[:5]:  # 只显示前5个错误
                    print(f"      • {error}")
                return {'encoding_issue': True, 'errors': serious_errors}
            else:
                print(f"   ✅ 未发现严重编码错误")
                if stderr:
                    print(f"   ℹ️ 一些警告信息: {len(error_lines)} 行")
                return {'encoding_issue': False, 'warnings': len(error_lines)}
        else:
            print(f"   ✅ 文件编码完整")
            return {'encoding_issue': False, 'warnings': 0}
            
    except Exception as e:
        print(f"   ❌ 检查编码时出错: {e}")
        return {'encoding_issue': True, 'error': str(e)}

def comprehensive_video_check(video_path):
    """综合视频质量检查"""
    print(f"🎬 综合视频质量检查")
    print("=" * 60)
    
    if not Path(video_path).exists():
        print(f"❌ 视频文件不存在: {video_path}")
        return
    
    # 各项检查
    basic_info = analyze_video_technical_info(video_path)
    sync_info = check_audio_video_sync(video_path)
    frame_info = detect_frame_issues(video_path)
    audio_info = check_audio_continuity(video_path)
    encoding_info = check_encoding_errors(video_path)
    
    # 综合评估
    print(f"\n📋 综合评估报告:")
    print("=" * 30)
    
    issues = []
    warnings = []
    
    # 检查各项结果
    if basic_info.get('has_issues'):
        issues.append("基本信息获取失败")
    
    if sync_info.get('sync_issue'):
        if sync_info.get('sync_diff', 0) > 1.0:
            issues.append(f"音视频严重不同步 ({sync_info.get('sync_diff', 0):.3f}秒)")
        else:
            warnings.append(f"音视频轻微不同步 ({sync_info.get('sync_diff', 0):.3f}秒)")
    
    if frame_info.get('frame_issue'):
        if frame_info.get('variance', 0) > 0.01:
            issues.append("帧率严重不稳定")
        else:
            warnings.append("帧率轻微不稳定")
    
    if audio_info.get('audio_issue'):
        if audio_info.get('large_gaps', 0) > 5:
            issues.append(f"音频多处中断 ({audio_info.get('large_gaps')}次)")
        elif audio_info.get('large_gaps', 0) > 0:
            warnings.append(f"音频偶尔中断 ({audio_info.get('large_gaps')}次)")
    
    if encoding_info.get('encoding_issue'):
        if len(encoding_info.get('errors', [])) > 10:
            issues.append("严重编码错误")
        else:
            warnings.append("轻微编码问题")
    
    # 输出评估结果
    if not issues and not warnings:
        print("✅ 视频质量优秀，未发现问题")
    elif not issues:
        print("⚠️ 视频质量良好，有一些小问题:")
        for warning in warnings:
            print(f"   • {warning}")
    else:
        print("❌ 视频存在问题:")
        for issue in issues:
            print(f"   🚨 {issue}")
        if warnings:
            print("   其他警告:")
            for warning in warnings:
                print(f"   • {warning}")
    
    # 建议
    print(f"\n💡 优化建议:")
    if sync_info.get('sync_issue'):
        print("   📝 音视频同步问题 → 调整FFmpeg的 -async 或 -vsync 参数")
    if frame_info.get('frame_issue'):
        print("   📝 帧率问题 → 避免使用 -r 参数强制帧率")
    if audio_info.get('audio_issue'):
        print("   📝 音频问题 → 检查源视频音频格式，考虑音频重新编码")
    if encoding_info.get('encoding_issue'):
        print("   📝 编码问题 → 使用 -c copy 避免重新编码，或检查源文件")

def test_merge_quality():
    """测试合并视频质量"""
    print("🧪 开始合并视频质量测试")
    print("=" * 60)
    
    # 先用广告文件夹的几个视频进行小规模测试
    ads_folder = Path("videos/downloads/ai_vanvan/2025-08-27/广告")
    
    if not ads_folder.exists():
        print("❌ 广告文件夹不存在")
        return
    
    video_files = list(ads_folder.glob("*.mp4"))
    if len(video_files) < 3:
        print("❌ 广告文件夹中视频文件不足")
        return
    
    # 选择前3个视频进行测试
    test_videos = sorted(video_files)[:3]
    
    print(f"📁 测试视频:")
    for i, video in enumerate(test_videos, 1):
        size = video.stat().st_size / (1024*1024)
        print(f"   {i}. {video.name} ({size:.1f}MB)")
    
    # 执行合并
    from src.utils.video_merger import VideoMerger
    
    merger = VideoMerger("ai_vanvan")
    output_path = f"videos/merged/ai_vanvan/quality_test_{datetime.now().strftime('%H-%M-%S')}.mp4"
    
    print(f"\n🔄 开始合并...")
    success = merger.merge_videos_with_ffmpeg(test_videos, output_path)
    
    if success and Path(output_path).exists():
        print(f"✅ 合并完成: {output_path}")
        
        # 检查合并后的视频质量
        comprehensive_video_check(output_path)
    else:
        print(f"❌ 合并失败")

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) > 1:
        # 检查指定的视频文件
        video_path = sys.argv[1]
        comprehensive_video_check(video_path)
    else:
        # 执行合并测试
        test_merge_quality()
