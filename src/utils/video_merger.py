"""
视频合并工具
"""
import os
import subprocess
import glob
import json
from datetime import datetime
from typing import Dict, List, Any

from .folder_manager import FolderManager
from .logger import Logger


class VideoMerger:
    """视频合并器"""
    
    def __init__(self, account_name: str = None):
        self.account_name = account_name
        self.logger = Logger(account_name) if account_name else Logger("video_merger")
        
        # 合并记录文件路径 - 统一放到 videos/logs 目录
        if account_name:
            logs_dir = os.path.join("videos", "logs")
            os.makedirs(logs_dir, exist_ok=True)
            self.merged_record_file = os.path.join(logs_dir, f"{account_name}_merged_record.json")
        else:
            self.merged_record_file = None
        
        # 简化版FolderManager，不需要完整配置
        if account_name:
            # 从main.py加载配置
            try:
                from main import load_account_config
                account_configs = load_account_config()
                config = account_configs.get(account_name, {})
                self.folder_manager = FolderManager(account_name, config)
            except:
                # 如果加载失败，使用None，后面直接构建路径
                self.folder_manager = None
        else:
            self.folder_manager = None
    
    def load_merged_record(self) -> Dict[str, Any]:
        """加载已合并视频记录"""
        if not self.merged_record_file or not os.path.exists(self.merged_record_file):
            return {"merged_videos": []}
        
        try:
            with open(self.merged_record_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"加载合并记录失败: {e}")
            return {"merged_videos": []}
    
    def save_merged_record(self, record: Dict[str, Any]):
        """保存已合并视频记录"""
        if not self.merged_record_file:
            return
        
        try:
            with open(self.merged_record_file, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存合并记录失败: {e}")
    
    def add_merged_videos(self, video_paths: List[str], output_path: str):
        """添加已合并的视频记录"""
        record = self.load_merged_record()
        
        merge_info = {
            "timestamp": datetime.now().isoformat(),
            "output_file": output_path,
            "input_videos": [os.path.abspath(v) for v in video_paths],
            "input_count": len(video_paths)
        }
        
        record["merged_videos"].append(merge_info)
        self.save_merged_record(record)
        self.logger.info(f"记录已合并视频: {len(video_paths)} 个文件 -> {os.path.basename(output_path)}")
    
    def is_video_merged(self, video_path: str) -> bool:
        """检查视频是否已经被合并过"""
        record = self.load_merged_record()
        video_abs_path = os.path.abspath(video_path)
        
        for merge_info in record["merged_videos"]:
            if video_abs_path in merge_info.get("input_videos", []):
                return True
        return False
    
    def get_latest_videos(self, directory: str, count: int = 8) -> List[str]:
        """获取最新的N个视频文件"""
        video_files = glob.glob(os.path.join(directory, "*.mp4"))
        
        # 按修改时间排序，最新的在前
        video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return video_files[:count]

    def get_video_resolution(self, video_path: str) -> tuple:
        """获取视频分辨率"""
        try:
            ffprobe_exe = os.path.join("tools", "ffmpeg", "bin", "ffprobe.exe")
            cmd = [
                ffprobe_exe,
                "-v", "quiet",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "csv=p=0",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            width, height = result.stdout.strip().split(',')
            return int(width), int(height)
        except Exception as e:
            self.logger.warning(f"无法获取视频分辨率 {video_path}: {e}")
            return None, None

    def find_target_resolution(self, video_files: List[str]) -> tuple:
        """分析所有视频，找到最适合的目标分辨率"""
        resolutions = {}
        
        for video in video_files:
            width, height = self.get_video_resolution(video)
            if width and height:
                # 判断是横屏还是竖屏
                if height > width:  # 竖屏
                    # 标准化竖屏分辨率
                    if width >= 720:
                        target = (720, 1280)  # 720p竖屏
                    else:
                        target = (540, 960)   # 较小竖屏
                else:  # 横屏
                    # 标准化横屏分辨率
                    if width >= 1280:
                        target = (1280, 720)  # 720p横屏
                    else:
                        target = (960, 540)   # 较小横屏
                        
                resolutions[target] = resolutions.get(target, 0) + 1
        
        if not resolutions:
            # 默认竖屏分辨率(Instagram常用)
            return 720, 1280
            
        # 返回最常见的分辨率
        target = max(resolutions.items(), key=lambda x: x[1])[0]
        self.logger.info(f"检测到目标分辨率: {target[0]}x{target[1]} (出现{resolutions[target]}次)")
        return target

    def ultimate_video_standardization(self, input_path: str, output_path: str, target_width: int, target_height: int) -> bool:
        """终极视频标准化：修复所有问题并统一参数"""
        try:
            ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
            
            # 终极修复命令
            cmd = [
                ffmpeg_exe,
                "-i", input_path,
                # 修复时间戳问题
                "-avoid_negative_ts", "make_zero",      # 将负时间戳设为0
                "-fflags", "+genpts",                   # 重新生成时间戳
                # 视频处理
                "-vf", f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black",
                "-c:v", "libx264",                      # 统一视频编码
                "-crf", "23",                           # 高质量
                "-preset", "medium",                    # 平衡速度和质量
                "-profile:v", "high",                   # 高配置
                "-level", "4.0",                        # 兼容性级别
                "-pix_fmt", "yuv420p",                  # 统一像素格式
                "-r", "30",                             # 统一帧率为30fps
                # 音频处理
                "-c:a", "aac",                          # 统一音频编码
                "-b:a", "128k",                         # 统一音频比特率
                "-ar", "44100",                         # 统一采样率
                "-ac", "2",                             # 统一声道数
                "-sample_fmt", "fltp",                  # 统一音频格式
                # 其他修复参数
                "-max_muxing_queue_size", "1024",       # 增大缓冲区
                "-vsync", "1",                          # 视频同步
                "-async", "1",                          # 音频同步
                "-y",                                   # 覆盖输出
                output_path
            ]
            
            self.logger.info(f"标准化视频: {os.path.basename(input_path)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if os.path.exists(output_path):
                    output_size_mb = os.path.getsize(output_path) / (1024*1024)
                    self.logger.info(f"标准化成功: {os.path.basename(input_path)} ({output_size_mb:.1f}MB)")
                    return True
                else:
                    self.logger.error(f"标准化失败: 输出文件不存在")
                    return False
            else:
                self.logger.error(f"标准化失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"标准化出错: {e}")
            return False

    def merge_videos_with_standardization(self, video_files: List[str], output_path: str) -> bool:
        """统一标准化后合并视频"""
        if not video_files:
            return False
            
        # 1. 分析目标分辨率
        target_width, target_height = self.find_target_resolution(video_files)
        self.logger.info(f"目标分辨率: {target_width}x{target_height}")
        
        # 2. 创建临时目录
        temp_dir = "temp/ultimate_standardized"
        os.makedirs(temp_dir, exist_ok=True)
        
        standardized_files = []
        
        try:
            # 3. 终极标准化所有视频
            self.logger.info("开始终极标准化视频...")
            for i, video in enumerate(video_files):
                temp_output = os.path.join(temp_dir, f"ultimate_{i:03d}.mp4")
                
                self.logger.info(f"  标准化 ({i+1}/{len(video_files)}): {os.path.basename(video)}")
                
                if self.ultimate_video_standardization(video, temp_output, target_width, target_height):
                    standardized_files.append(temp_output)
                else:
                    self.logger.warning(f"跳过标准化失败的视频: {video}")
            
            if not standardized_files:
                self.logger.error("没有成功标准化的视频")
                return False
                
            # 4. 安全合并标准化后的视频
            self.logger.info("开始合并标准化后的视频...")
            return self.merge_videos_with_ffmpeg(standardized_files, output_path)
            
        finally:
            # 5. 清理临时文件
            for temp_file in standardized_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            if os.path.exists(temp_dir):
                try:
                    os.rmdir(temp_dir)
                except:
                    pass

    def merge_videos_with_ffmpeg(self, video_files: List[str], output_path: str) -> bool:
        """使用FFmpeg合并视频"""
        if not video_files:
            self.logger.warning("没有视频文件需要合并")
            return False
        
        self.logger.info(f"准备合并 {len(video_files)} 个视频文件:")
        for i, video in enumerate(video_files, 1):
            size_mb = os.path.getsize(video) / (1024*1024)
            self.logger.info(f"  {i}. {os.path.basename(video)} ({size_mb:.1f}MB)")
        
        # 创建临时文件列表
        filelist_path = "temp_filelist.txt"
        
        try:
            # 写入文件列表
            with open(filelist_path, 'w', encoding='utf-8') as f:
                for video in video_files:
                    # 使用绝对路径并转义
                    abs_path = os.path.abspath(video).replace('\\', '/')
                    f.write(f"file '{abs_path}'\n")
            
            # 检查FFmpeg
            ffmpeg_paths = [
                os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe"),
                "ffmpeg"
            ]
            
            ffmpeg_exe = None
            for path in ffmpeg_paths:
                if os.path.exists(path):
                    ffmpeg_exe = path
                    break
            
            if not ffmpeg_exe:
                ffmpeg_exe = "ffmpeg"
            
            # FFmpeg合并命令
            cmd = [
                ffmpeg_exe,
                "-f", "concat",
                "-safe", "0",
                "-i", filelist_path,
                "-c", "copy",
                "-y",  # 覆盖输出文件
                output_path
            ]
            
            self.logger.info(f"开始合并视频到: {output_path}")
            
            # 执行FFmpeg命令
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 计算输出文件大小
                output_size_mb = os.path.getsize(output_path) / (1024*1024)
                self.logger.success(f"合并成功! 输出文件: {output_path} ({output_size_mb:.1f}MB)")
                return True
            else:
                self.logger.error(f"FFmpeg合并失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"合并过程出错: {e}")
            return False
        finally:
            # 清理临时文件
            if os.path.exists(filelist_path):
                os.remove(filelist_path)

    def merge_unmerged_videos(self, limit: int = None) -> Dict[str, int]:
        """合并未合并的视频（使用终极标准化模式）"""
        if not self.account_name:
            return {"merged": 0, "skipped": 0, "failed": 1}
        
        # 获取所有下载目录
        downloads_base = os.path.join("videos", "downloads", self.account_name)
        
        if not os.path.exists(downloads_base):
            self.logger.warning(f"下载目录不存在: {downloads_base}")
            return {"merged": 0, "skipped": 0, "failed": 0}
        
        # 只收集今天的视频文件（新下载的）
        today = datetime.now().strftime("%Y-%m-%d")
        today_path = os.path.join(downloads_base, today)
        
        all_today_videos = []
        if os.path.exists(today_path):
            videos = glob.glob(os.path.join(today_path, "*.mp4"))
            all_today_videos.extend(videos)
        
        if not all_today_videos:
            self.logger.info("没有找到今天新下载的视频文件")
            return {"merged": 0, "skipped": 0, "failed": 0}
        
        # **关键改进：过滤掉已经被合并过的视频**
        unmerged_videos = []
        skipped_count = 0
        for video in all_today_videos:
            if self.is_video_merged(video):
                skipped_count += 1
                # 已合并的视频不需要记录日志，避免噪音
            else:
                unmerged_videos.append(video)
        
        if skipped_count > 0:
            self.logger.info(f"今天找到 {len(all_today_videos)} 个视频，其中 {skipped_count} 个已合并，{len(unmerged_videos)} 个待合并")
        
        if not unmerged_videos:
            self.logger.info("今天所有视频都已经合并过了，无需重复合并")
            return {"merged": 0, "skipped": skipped_count, "failed": 0}
        
        # 按修改时间排序，最新的在前
        unmerged_videos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # 应用数量限制
        if limit:
            merge_videos = unmerged_videos[:limit]
            self.logger.info(f"准备合并最新的 {len(merge_videos)} 个视频（剩余 {len(unmerged_videos) - len(merge_videos)} 个）")
        else:
            merge_videos = unmerged_videos
            self.logger.info(f"准备合并全部 {len(unmerged_videos)} 个未合并视频")
        
        # 创建合并输出目录
        merge_dir = os.path.join("videos", "merged", self.account_name)
        os.makedirs(merge_dir, exist_ok=True)
        
        # 生成输出文件名 - 简化格式：只保留日期时间
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"{timestamp}.mp4"
        output_path = os.path.join(merge_dir, output_filename)
        
        # 使用终极标准化合并（包含所有功能）
        self.logger.info("🎯 使用终极标准化合并模式")
        self.logger.info("📋 包含功能: 统一分辨率(黑边) + AAC音频 + 时间戳修复 + 参数标准化")
        
        # 生成一个临时合并文件用于终极标准化
        temp_merge_path = output_path.replace('.mp4', '_temp.mp4')
        
        # 先使用终极标准化合并
        success = self.merge_videos_with_standardization(merge_videos, output_path)
        
        # 执行合并
        if success:
            # **关键改进：记录已合并的视频**
            self.add_merged_videos(merge_videos, output_path)
            return {"merged": 1, "skipped": skipped_count, "failed": 0}
        else:
            return {"merged": 0, "skipped": skipped_count, "failed": 1}
