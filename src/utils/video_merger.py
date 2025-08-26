"""
视频合并工具
"""
import os
import subprocess
import glob
from datetime import datetime
from typing import Dict, List, Any

from .folder_manager import FolderManager
from .logger import Logger


class VideoMerger:
    """视频合并器"""
    
    def __init__(self, account_name: str = None):
        self.account_name = account_name
        self.logger = Logger(account_name) if account_name else Logger("video_merger")
        
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
    
    def get_latest_videos(self, directory: str, count: int = 8) -> List[str]:
        """获取最新的N个视频文件"""
        video_files = glob.glob(os.path.join(directory, "*.mp4"))
        
        # 按修改时间排序，最新的在前
        video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return video_files[:count]

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
        """合并未合并的视频"""
        # 暂时的简单实现
        if not self.account_name:
            return {"merged": 0, "skipped": 0, "failed": 1}
        
        # 获取今天的下载目录
        today = datetime.now().strftime("%Y-%m-%d")
        download_dir = os.path.join("videos", "downloads", self.account_name, today)
        
        if not os.path.exists(download_dir):
            self.logger.warning(f"下载目录不存在: {download_dir}")
            return {"merged": 0, "skipped": 0, "failed": 0}
        
        # 获取要合并的视频数量
        merge_count = limit if limit else 8
        
        # 获取最新的视频文件
        video_files = self.get_latest_videos(download_dir, merge_count)
        
        if not video_files:
            self.logger.info("没有找到需要合并的视频文件")
            return {"merged": 0, "skipped": 0, "failed": 0}
        
        # 创建合并输出目录
        merge_dir = os.path.join("videos", "merged", self.account_name)
        os.makedirs(merge_dir, exist_ok=True)
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"{self.account_name}_{timestamp}_merged_{len(video_files)}videos.mp4"
        output_path = os.path.join(merge_dir, output_filename)
        
        # 执行合并
        if self.merge_videos_with_ffmpeg(video_files, output_path):
            return {"merged": 1, "skipped": 0, "failed": 0}
        else:
            return {"merged": 0, "skipped": 0, "failed": 1}

    def merge_videos(self, input_files, output_file):
        """合并视频文件 - 兼容性方法"""
        return self.merge_videos_with_ffmpeg(input_files, output_file)
