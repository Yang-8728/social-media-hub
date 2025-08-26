"""
日志工具
统一的日志记录和管理
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class Logger:
    """日志记录器"""
    
    def __init__(self, account_name: str):
        self.account_name = account_name
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # 日志文件按日期命名
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.logs_dir / f"{today}-{account_name}.log"
        
        # 下载记录文件
        self.download_log_file = Path("videos") / "download_logs" / f"{account_name}_downloads.json"
        self.download_log_file.parent.mkdir(parents=True, exist_ok=True)
        
    def log(self, level: str, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # 打印到控制台
        print(log_entry)
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def info(self, message: str):
        """信息日志"""
        self.log("INFO", message)
    
    def success(self, message: str):
        """成功日志"""
        self.log("SUCCESS", message)
    
    def warning(self, message: str):
        """警告日志"""
        self.log("WARNING", message)
    
    def error(self, message: str):
        """错误日志"""
        self.log("ERROR", message)
    
    def load_download_log(self) -> Dict[str, Any]:
        """加载下载记录"""
        if self.download_log_file.exists():
            with open(self.download_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "account": self.account_name,
            "downloads": [],
            "merged_sessions": []
        }
    
    def save_download_log(self, log_data: Dict[str, Any]):
        """保存下载记录"""
        with open(self.download_log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2, default=str)
    
    def record_download(self, shortcode: str, status: str, file_path: str = "", error: str = "", folder: str = "", blogger: str = ""):
        """记录下载信息"""
        log_data = self.load_download_log()
        
        download_record = {
            "shortcode": shortcode,
            "download_time": datetime.now().isoformat(),
            "status": status,  # "success", "failed", "skipped"
            "file_path": file_path,
            "error": error,
            "merged": False,  # 是否已合并
            "download_folder": folder,  # 下载文件夹
            "blogger_name": blogger  # 博主名字
        }
        
        # 检查是否已存在，避免重复记录
        existing = next((d for d in log_data["downloads"] if d["shortcode"] == shortcode), None)
        if existing:
            existing.update(download_record)
        else:
            log_data["downloads"].append(download_record)
        
        self.save_download_log(log_data)
        
        # 移除自动打印下载记录信息，由调用者决定是否显示
        # if status == "success":
        #     self.success(f"下载记录: {shortcode} -> {file_path}")
        # elif status == "failed":
        #     self.error(f"下载失败: {shortcode} - {error}")
        # else:
        #     self.warning(f"下载跳过: {shortcode}")
        
        # 移除文件夹和博主信息的自动打印
        # if folder:
        #     self.info(f"文件夹: {folder}")
        # if blogger:
        #     self.info(f"博主: {blogger}")
    
    def get_unmerged_downloads(self) -> List[str]:
        """获取未合并的下载记录，按下载时间倒序排列（最新的在前）"""
        log_data = self.load_download_log()
        unmerged = [d for d in log_data["downloads"] if d["status"] == "success" and not d["merged"]]
        
        # 按下载时间排序，最新的在前
        unmerged.sort(key=lambda x: x.get("download_time", ""), reverse=True)
        
        # 返回shortcode列表
        return [d["shortcode"] for d in unmerged]
    
    def mark_as_merged(self, shortcode: str, merged_file_path: str):
        """标记单个视频为已合并"""
        log_data = self.load_download_log()
        
        # 更新下载记录
        for download in log_data["downloads"]:
            if download["shortcode"] == shortcode:
                download["merged"] = True
                break
        
        # 记录合并会话
        merge_session = {
            "merge_time": datetime.now().isoformat(),
            "shortcode": shortcode,
            "merged_file": merged_file_path
        }
        log_data["merged_sessions"].append(merge_session)
        
        self.save_download_log(log_data)
        self.success(f"标记为已合并: {shortcode} -> {merged_file_path}")
    
    def mark_batch_as_merged(self, shortcodes: List[str], merged_file_path: str):
        """标记多个视频为已合并（批量合并时使用）"""
        log_data = self.load_download_log()
        
        # 更新下载记录
        for download in log_data["downloads"]:
            if download["shortcode"] in shortcodes:
                download["merged"] = True
        
        # 记录合并会话
        merge_session = {
            "merge_time": datetime.now().isoformat(),
            "shortcodes": shortcodes,
            "merged_file": merged_file_path,
            "video_count": len(shortcodes)
        }
        log_data["merged_sessions"].append(merge_session)
        
        self.save_download_log(log_data)
        self.success(f"批量合并完成: {len(shortcodes)} 个视频 -> {merged_file_path}")
    
    def get_download_summary(self) -> str:
        """获取下载汇总信息"""
        log_data = self.load_download_log()
        downloads = log_data["downloads"]
        
        total = len(downloads)
        success = len([d for d in downloads if d["status"] == "success"])
        failed = len([d for d in downloads if d["status"] == "failed"])
        merged = len([d for d in downloads if d.get("merged", False)])
        unmerged = success - merged
        
        return f"下载汇总: 总计 {total}, 成功 {success}, 失败 {failed}, 已合并 {merged}, 待合并 {unmerged}"
    
    def is_downloaded(self, shortcode: str) -> bool:
        """检查指定shortcode是否已下载"""
        log_data = self.load_download_log()
        downloads = log_data["downloads"]
        
        # 检查是否存在成功下载的记录
        return any(d["shortcode"] == shortcode and d["status"] == "success" for d in downloads)
