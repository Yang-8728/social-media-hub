"""
检查当前下载和合并状态
"""
import json
import os

def check_status():
    # 读取ai_vanvan数据
    with open('videos/download_logs/ai_vanvan_downloads.json', 'r', encoding='utf-8') as f:
        ai_vanvan_data = json.load(f)
    
    # 读取aigf8728数据
    with open('videos/download_logs/aigf8728_downloads.json', 'r', encoding='utf-8') as f:
        aigf8728_data = json.load(f)
    
    # 统计ai_vanvan
    ai_vanvan_total = len(ai_vanvan_data['downloads'])
    ai_vanvan_unmerged = sum(1 for d in ai_vanvan_data['downloads'] if not d.get('merged', False))
    
    # 统计aigf8728
    aigf8728_total = len(aigf8728_data['downloads'])
    aigf8728_unmerged = sum(1 for d in aigf8728_data['downloads'] if not d.get('merged', False))
    
    print('📊 当前状态总结：')
    print(f'ai_vanvan (搞笑): {ai_vanvan_total}个视频，{ai_vanvan_unmerged}个未合并')
    print(f'aigf8728 (女朋友): {aigf8728_total}个视频，{aigf8728_unmerged}个未合并')
    print()
    
    # 检查视频文件存在情况
    ai_vanvan_video_count = 0
    aigf8728_video_count = 0
    
    if os.path.exists('videos/downloads/ai_vanvan'):
        for root, dirs, files in os.walk('videos/downloads/ai_vanvan'):
            ai_vanvan_video_count += len([f for f in files if f.endswith('.mp4')])
    
    if os.path.exists('videos/downloads/aigf8728'):
        for root, dirs, files in os.walk('videos/downloads/aigf8728'):
            aigf8728_video_count += len([f for f in files if f.endswith('.mp4')])
    
    print(f'ai_vanvan 实际视频文件: {ai_vanvan_video_count}个')
    print(f'aigf8728 实际视频文件: {aigf8728_video_count}个')
    
    return {
        'ai_vanvan': {'total': ai_vanvan_total, 'unmerged': ai_vanvan_unmerged, 'files': ai_vanvan_video_count},
        'aigf8728': {'total': aigf8728_total, 'unmerged': aigf8728_unmerged, 'files': aigf8728_video_count}
    }

if __name__ == "__main__":
    check_status()
