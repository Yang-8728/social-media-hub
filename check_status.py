"""
检查当前下载和合并状态
"""
import json

def check_status():
    # 读取gaoxiao数据
    with open('videos/download_logs/gaoxiao_downloads.json', 'r', encoding='utf-8') as f:
        gaoxiao_data = json.load(f)
    
    # 读取gf数据
    with open('videos/download_logs/gf_downloads.json', 'r', encoding='utf-8') as f:
        gf_data = json.load(f)
    
    # 统计gaoxiao
    gaoxiao_total = len(gaoxiao_data['downloads'])
    gaoxiao_unmerged = sum(1 for d in gaoxiao_data['downloads'] if not d.get('merged', False))
    
    # 统计gf
    gf_total = len(gf_data['downloads'])
    gf_unmerged = sum(1 for d in gf_data['downloads'] if not d.get('merged', False))
    
    print('📊 当前状态总结：')
    print(f'gaoxiao (搞笑): {gaoxiao_total}个视频，{gaoxiao_unmerged}个未合并')
    print(f'gf (女朋友): {gf_total}个视频，{gf_unmerged}个未合并')
    print()
    
    # 检查视频文件存在情况
    import os
    gaoxiao_video_count = 0
    gf_video_count = 0
    
    if os.path.exists('videos/downloads/gaoxiao'):
        for root, dirs, files in os.walk('videos/downloads/gaoxiao'):
            gaoxiao_video_count += len([f for f in files if f.endswith('.mp4')])
    
    if os.path.exists('videos/downloads/gf'):
        for root, dirs, files in os.walk('videos/downloads/gf'):
            gf_video_count += len([f for f in files if f.endswith('.mp4')])
    
    print(f'gaoxiao 实际视频文件: {gaoxiao_video_count}个')
    print(f'gf 实际视频文件: {gf_video_count}个')
    
    return {
        'gaoxiao': {'total': gaoxiao_total, 'unmerged': gaoxiao_unmerged, 'files': gaoxiao_video_count},
        'gf': {'total': gf_total, 'unmerged': gf_unmerged, 'files': gf_video_count}
    }

if __name__ == "__main__":
    check_status()
