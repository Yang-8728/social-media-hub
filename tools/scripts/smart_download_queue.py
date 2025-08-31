"""
智能下载队列管理
优化ai_vanvan的下载体验
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class SmartDownloadQueue:
    """智能下载队列"""
    
    def __init__(self, account_name: str):
        self.account_name = account_name
        self.config_file = f"data/{account_name}_download_queue.json"
        
    def analyze_download_pattern(self) -> Dict:
        """分析下载模式"""
        log_file = f"data/download_logs/{self.account_name}_downloads.json"
        
        if not os.path.exists(log_file):
            return {"pattern": "new_user", "recommendation": "conservative"}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                downloads = data.get('downloads', [])
            
            # 分析最近7天的下载
            recent_downloads = []
            seven_days_ago = datetime.now() - timedelta(days=7)
            
            for download in downloads:
                try:
                    download_time = datetime.fromisoformat(download['download_time'].replace('Z', '+00:00'))
                    if download_time >= seven_days_ago:
                        recent_downloads.append(download)
                except:
                    continue
            
            total_recent = len(recent_downloads)
            success_recent = len([d for d in recent_downloads if d.get('status') == 'success'])
            
            # 根据成功率推荐策略
            if total_recent == 0:
                return {"pattern": "inactive", "recommendation": "conservative"}
            
            success_rate = success_recent / total_recent
            
            if success_rate >= 0.9 and total_recent >= 20:
                return {"pattern": "stable_heavy", "recommendation": "balanced"}
            elif success_rate >= 0.8:
                return {"pattern": "stable_normal", "recommendation": "balanced"}
            else:
                return {"pattern": "unstable", "recommendation": "conservative"}
                
        except Exception as e:
            return {"pattern": "error", "recommendation": "conservative", "error": str(e)}
    
    def get_optimal_settings(self) -> Dict:
        """获取最优下载设置"""
        pattern_analysis = self.analyze_download_pattern()
        
        settings_map = {
            "conservative": {
                "max_posts_per_session": 10,
                "request_delay": 5,
                "batch_size": 3,
                "batch_delay": 15
            },
            "balanced": {
                "max_posts_per_session": 30,
                "request_delay": 3,
                "batch_size": 5,
                "batch_delay": 10
            },
            "aggressive": {
                "max_posts_per_session": 50,
                "request_delay": 2,
                "batch_size": 8,
                "batch_delay": 5
            }
        }
        
        recommendation = pattern_analysis.get("recommendation", "conservative")
        settings = settings_map.get(recommendation, settings_map["conservative"])
        settings["pattern"] = pattern_analysis.get("pattern")
        
        return settings
    
    def suggest_download_time(self) -> str:
        """建议下载时间"""
        # 分析历史成功时间段
        log_file = f"data/download_logs/{self.account_name}_downloads.json"
        
        if not os.path.exists(log_file):
            return "建议在用网低峰期(深夜或早晨)进行下载"
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                downloads = data.get('downloads', [])
            
            # 统计成功下载的时间分布
            hour_success = {}
            for download in downloads:
                if download.get('status') == 'success':
                    try:
                        download_time = datetime.fromisoformat(download['download_time'].replace('Z', '+00:00'))
                        hour = download_time.hour
                        hour_success[hour] = hour_success.get(hour, 0) + 1
                    except:
                        continue
            
            if not hour_success:
                return "建议在用网低峰期进行下载"
            
            # 找出成功率最高的时间段
            best_hour = max(hour_success, key=hour_success.get)
            
            if 22 <= best_hour or best_hour <= 6:
                return f"建议在深夜时段下载 (最佳时间: {best_hour}:00)"
            elif 6 < best_hour <= 9:
                return f"建议在早晨时段下载 (最佳时间: {best_hour}:00)"
            else:
                return f"建议在用网低峰期下载 (历史最佳: {best_hour}:00)"
                
        except Exception:
            return "建议在用网低峰期进行下载"

# 为ai_vanvan生成优化报告
def generate_optimization_report(account_name: str = "ai_vanvan"):
    """生成优化报告"""
    queue = SmartDownloadQueue(account_name)
    
    print(f"🔍 {account_name} 下载优化分析报告")
    print("=" * 50)
    
    # 分析下载模式
    pattern = queue.analyze_download_pattern()
    print(f"📊 下载模式: {pattern.get('pattern', 'unknown')}")
    print(f"🎯 推荐策略: {pattern.get('recommendation', 'conservative')}")
    
    # 获取最优设置
    settings = queue.get_optimal_settings()
    print(f"\n⚙️  推荐设置:")
    print(f"  - 每次最大下载: {settings['max_posts_per_session']} 个")
    print(f"  - 请求延迟: {settings['request_delay']} 秒")
    print(f"  - 批处理大小: {settings['batch_size']} 个")
    print(f"  - 批次延迟: {settings['batch_delay']} 秒")
    
    # 时间建议
    time_suggestion = queue.suggest_download_time()
    print(f"\n⏰ 时间建议: {time_suggestion}")
    
    print("=" * 50)

if __name__ == "__main__":
    generate_optimization_report()
