"""
视频质量检测工具
检测常见的合并视频问题
"""
import os
import subprocess
import json
from typing import Dict, List, Tuple, Any

class VideoQualityChecker:
    """视频质量检测器"""
    
    def __init__(self):
        self.ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
        self.ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """获取视频详细信息"""
        try:
            cmd = [
                self.ffprobe_exe,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
            
        except Exception as e:
            print(f"❌ 获取视频信息失败: {e}")
            return {}
    
    def check_video_issues(self, video_path: str) -> Dict[str, Any]:
        """全面检查视频问题"""
        print(f"\n🔍 检查视频: {os.path.basename(video_path)}")
        
        issues = {
            "black_frames": False,
            "audio_sync": True,
            "resolution_issues": False,
            "framerate_issues": False,
            "corruption": False,
            "bilibili_compatible": True,
            "details": {}
        }
        
        # 获取基本信息
        info = self.get_video_info(video_path)
        if not info:
            issues["corruption"] = True
            return issues
        
        # 检查视频流和音频流
        video_stream = None
        audio_stream = None
        
        for stream in info.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream
            elif stream.get("codec_type") == "audio":
                audio_stream = stream
        
        if not video_stream:
            print("❌ 没有找到视频流")
            issues["corruption"] = True
            return issues
        
        # 1. 检查分辨率
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        
        print(f"📐 分辨率: {width}x{height}")
        issues["details"]["resolution"] = f"{width}x{height}"
        
        # 检查是否是奇怪的分辨率
        if width % 2 != 0 or height % 2 != 0:
            print("⚠️  警告: 分辨率不是偶数，可能导致兼容性问题")
            issues["resolution_issues"] = True
        
        # 2. 检查帧率
        fps_str = video_stream.get("r_frame_rate", "0/1")
        try:
            num, den = map(int, fps_str.split('/'))
            fps = num / den if den != 0 else 0
            print(f"🎬 帧率: {fps:.2f} fps")
            issues["details"]["framerate"] = fps
            
            # B站推荐帧率检查
            if fps < 23 or fps > 61:
                print(f"⚠️  警告: 帧率 {fps:.2f} fps 可能不符合B站要求(推荐24-60fps)")
                issues["framerate_issues"] = True
                issues["bilibili_compatible"] = False
                
        except Exception as e:
            print(f"⚠️  无法解析帧率: {fps_str}")
            issues["framerate_issues"] = True
        
        # 3. 检查音频
        if audio_stream:
            sample_rate = audio_stream.get("sample_rate")
            channels = audio_stream.get("channels")
            print(f"🔊 音频: {sample_rate}Hz, {channels}声道")
            issues["details"]["audio"] = f"{sample_rate}Hz, {channels}ch"
        else:
            print("⚠️  没有音频流")
            issues["details"]["audio"] = "无音频"
        
        # 4. 检查编码
        video_codec = video_stream.get("codec_name")
        audio_codec = audio_stream.get("codec_name") if audio_stream else "none"
        
        print(f"🎥 视频编码: {video_codec}")
        print(f"🔊 音频编码: {audio_codec}")
        
        issues["details"]["video_codec"] = video_codec
        issues["details"]["audio_codec"] = audio_codec
        
        # B站兼容性检查
        if video_codec not in ["h264", "libx264"]:
            print(f"⚠️  视频编码 {video_codec} 可能不被B站支持")
            issues["bilibili_compatible"] = False
        
        if audio_codec not in ["aac", "mp3"] and audio_codec != "none":
            print(f"⚠️  音频编码 {audio_codec} 可能不被B站支持")
            issues["bilibili_compatible"] = False
        
        # 5. 检查时长
        duration = float(info.get("format", {}).get("duration", 0))
        print(f"⏱️  时长: {duration:.2f}秒")
        issues["details"]["duration"] = duration
        
        if duration < 1:
            print("❌ 视频时长过短")
            issues["corruption"] = True
        
        # 6. 检查文件大小
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"📁 文件大小: {size_mb:.1f}MB")
        issues["details"]["size_mb"] = size_mb
        
        return issues
    
    def detect_black_frames(self, video_path: str, threshold: float = 0.1) -> bool:
        """检测黑屏帧"""
        try:
            print(f"🔍 检测黑屏帧...")
            
            cmd = [
                self.ffmpeg_exe,
                "-i", video_path,
                "-vf", f"blackdetect=d=0.5:pix_th={threshold}",
                "-f", "null",
                "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # 分析stderr中的blackdetect输出
            black_periods = []
            for line in result.stderr.split('\n'):
                if 'blackdetect' in line and 'black_start' in line:
                    black_periods.append(line.strip())
            
            if black_periods:
                print(f"⚠️  检测到 {len(black_periods)} 个黑屏片段:")
                for period in black_periods[:3]:  # 只显示前3个
                    print(f"     {period}")
                if len(black_periods) > 3:
                    print(f"     ... 还有 {len(black_periods)-3} 个")
                return True
            else:
                print("✅ 没有检测到明显的黑屏问题")
                return False
                
        except Exception as e:
            print(f"❌ 黑屏检测失败: {e}")
            return False
    
    def check_audio_video_sync(self, video_path: str) -> bool:
        """检查音画同步（简单版本）"""
        try:
            info = self.get_video_info(video_path)
            
            video_duration = None
            audio_duration = None
            
            for stream in info.get("streams", []):
                duration = float(stream.get("duration", 0))
                if stream.get("codec_type") == "video":
                    video_duration = duration
                elif stream.get("codec_type") == "audio":
                    audio_duration = duration
            
            if video_duration and audio_duration:
                diff = abs(video_duration - audio_duration)
                print(f"🎵 音画时长差异: {diff:.3f}秒")
                
                if diff > 0.1:  # 超过100ms认为可能有问题
                    print(f"⚠️  音画时长差异较大，可能存在同步问题")
                    return False
                else:
                    print("✅ 音画时长一致")
                    return True
            else:
                print("⚠️  无法比较音画时长")
                return True
                
        except Exception as e:
            print(f"❌ 音画同步检查失败: {e}")
            return True
    
    def comprehensive_check(self, video_path: str) -> Dict[str, Any]:
        """综合检查"""
        print(f"\n{'='*60}")
        print(f"📹 综合视频质量检查")
        print(f"{'='*60}")
        
        if not os.path.exists(video_path):
            return {"error": "文件不存在"}
        
        # 基本信息检查
        issues = self.check_video_issues(video_path)
        
        # 黑屏检测
        issues["black_frames"] = self.detect_black_frames(video_path)
        
        # 音画同步检查  
        issues["audio_sync"] = self.check_audio_video_sync(video_path)
        
        # 生成总结
        print(f"\n📊 检查结果总结:")
        print(f"✅ 分辨率兼容: {'是' if not issues['resolution_issues'] else '否'}")
        print(f"✅ 帧率兼容: {'是' if not issues['framerate_issues'] else '否'}")
        print(f"✅ 音画同步: {'是' if issues['audio_sync'] else '否'}")
        print(f"✅ 无黑屏: {'是' if not issues['black_frames'] else '否'}")
        print(f"✅ 无损坏: {'是' if not issues['corruption'] else '否'}")
        print(f"✅ B站兼容: {'是' if issues['bilibili_compatible'] else '否'}")
        
        # 总体评分
        score = 0
        total = 6
        
        if not issues['resolution_issues']: score += 1
        if not issues['framerate_issues']: score += 1  
        if issues['audio_sync']: score += 1
        if not issues['black_frames']: score += 1
        if not issues['corruption']: score += 1
        if issues['bilibili_compatible']: score += 1
        
        print(f"\n🎯 质量评分: {score}/{total} ({score/total*100:.0f}%)")
        
        if score == total:
            print("🎉 视频质量完美，可以上传到B站！")
        elif score >= 4:
            print("✅ 视频质量良好，基本可以使用")
        else:
            print("⚠️  视频存在多个质量问题，建议重新处理")
        
        return issues

# 使用示例
def check_merged_video(video_path: str):
    """检查合并后的视频"""
    checker = VideoQualityChecker()
    return checker.comprehensive_check(video_path)
