"""
智能下载队列 - 根据用户下载模式自动调整队列策略
"""
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

class SmartDownloadQueue:
    """智能下载队列"""
    
    def __init__(self, account_name: str):
        self.account_name = account_name
        
        # 获取项目根目录
        self.project_root = Path(__file__).parent.parent.parent
        
        # 设置配置文件路径
        config_dir = self.project_root / "logs" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = config_dir / f"{account_name}_download_queue.json"
        
    def analyze_download_pattern(self) -> Dict:
        """分析下载模式"""
        log_file = self.project_root / "logs" / "downloads" / f"{self.account_name}_downloads.json"
        
        if not os.path.exists(log_file):
            return {"pattern": "new_user", "recommendation": "conservative"}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                downloads = data.get('downloads', [])
            
            # 分析最近7天的下载
            recent_downloads = []
            cutoff_date = datetime.now() - timedelta(days=7)
            
            for download in downloads:
                download_date = datetime.strptime(download.get('timestamp', ''), '%Y-%m-%d %H:%M:%S')
                if download_date >= cutoff_date:
                    recent_downloads.append(download)
        
            # 计算统计数据
            total_recent = len(recent_downloads)
            success_recent = len([d for d in recent_downloads if d.get('status') == 'success'])
            
            if total_recent == 0:
                pattern = "inactive"
                recommendation = "conservative"
            elif success_recent / total_recent >= 0.8:
                pattern = "power_user"
                recommendation = "aggressive"
            elif success_recent / total_recent >= 0.5:
                pattern = "regular_user"
                recommendation = "balanced"
            else:
                pattern = "casual_user"
                recommendation = "conservative"
                
            return {
                "pattern": pattern,
                "recommendation": recommendation,
                "total_recent": total_recent,
                "success_recent": success_recent,
                "success_rate": success_recent / max(total_recent, 1)
            }
            
        except Exception as e:
            print(f"分析下载模式时出错: {e}")
            return {"pattern": "error", "recommendation": "conservative"}

    def get_queue_by_pattern(self, target_count: int) -> List[str]:
        """根据用户模式生成智能队列"""
        pattern_info = self.analyze_download_pattern()
        pattern = pattern_info.get("pattern", "new_user")
        
        # 根据模式调整队列策略
        if pattern == "power_user":
            # 大用户：更多最新内容
            queue = self._generate_aggressive_queue(target_count)
        elif pattern == "regular_user":
            # 普通用户：平衡策略
            queue = self._generate_balanced_queue(target_count)
        else:
            # 新用户/轻度用户：保守策略
            queue = self._generate_conservative_queue(target_count)
            
        return queue
    
    def _generate_aggressive_queue(self, count: int) -> List[str]:
        """生成激进队列：70%最新，30%精选旧内容"""
        recent_count = int(count * 0.7)
        old_count = count - recent_count
        
        return self._get_mixed_queue(recent_count, old_count, prefer_recent=True)
    
    def _generate_balanced_queue(self, count: int) -> List[str]:
        """生成平衡队列：50%最新，50%精选旧内容"""
        recent_count = int(count * 0.5)
        old_count = count - recent_count
        
        return self._get_mixed_queue(recent_count, old_count, prefer_recent=False)
    
    def _generate_conservative_queue(self, count: int) -> List[str]:
        """生成保守队列：30%最新，70%精选旧内容"""
        recent_count = int(count * 0.3)
        old_count = count - recent_count
        
        return self._get_mixed_queue(recent_count, old_count, prefer_recent=False)
    
    def _get_mixed_queue(self, recent_count: int, old_count: int, prefer_recent: bool) -> List[str]:
        """获取混合队列"""
        # 这里需要实际的Instagram数据获取逻辑
        # 暂时返回示例数据
        queue = []
        
        # 添加最新内容
        for i in range(recent_count):
            queue.append(f"recent_post_{i}")
            
        # 添加精选旧内容
        for i in range(old_count):
            queue.append(f"featured_old_post_{i}")
            
        return queue

    def save_queue_config(self, config: Dict):
        """保存队列配置"""
        try:
            os.makedirs(os.path.dirname(str(self.config_file)), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存队列配置失败: {e}")

    def load_queue_config(self) -> Dict:
        """加载队列配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载队列配置失败: {e}")
        
        return {}

    def get_unprocessed_from_log(self) -> List[Dict]:
        """从日志中获取未处理的下载"""
        log_file = self.project_root / "logs" / "downloads" / f"{self.account_name}_downloads.json"
        
        if not os.path.exists(log_file):
            return []
            
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                downloads = data.get('downloads', [])
            
            # 查找状态为pending或failed的下载
            unprocessed = []
            for download in downloads:
                if download.get('status') in ['pending', 'failed', 'error']:
                    unprocessed.append(download)
            
            return unprocessed
            
        except Exception as e:
            print(f"获取未处理下载时出错: {e}")
            return []