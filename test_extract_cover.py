"""
测试提取视频封面
"""
import os
import subprocess
import glob

def extract_cover_from_video(video_path, output_path):
    """从视频提取封面（第一帧）"""
    try:
        print(f"📸 提取封面：{os.path.basename(video_path)}")
        
        # 使用 ffmpeg 提取第一帧
        ffmpeg_exe = os.path.join("tools", "ffmpeg", "bin", "ffmpeg.exe")
        cmd = [
            ffmpeg_exe,
            "-i", video_path,
            "-ss", "00:00:00",  # 从第0秒开始
            "-vframes", "1",     # 只提取1帧
            "-q:v", "2",         # 高质量
            "-y",                # 覆盖已存在的文件
            output_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            cover_size_kb = os.path.getsize(output_path) / 1024
            print(f"✅ 封面已保存: {output_path}")
            print(f"📦 文件大小: {cover_size_kb:.1f} KB")
            return True
        else:
            print(f"❌ 封面提取失败")
            if result.stderr:
                print(f"错误信息: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 提取出错: {e}")
        return False

def test_extract_cover():
    """测试提取第 10 个视频的封面"""
    
    # 查找今天的视频
    video_dir = "videos/downloads/youtube/2026-02-06"
    
    if not os.path.exists(video_dir):
        print(f"❌ 视频目录不存在: {video_dir}")
        return
    
    # 获取所有视频文件
    video_files = glob.glob(os.path.join(video_dir, "*.mp4"))
    
    if not video_files:
        print(f"❌ 没有找到视频文件")
        return
    
    # 按修改时间排序
    video_files.sort(key=lambda x: os.path.getmtime(x))
    
    print(f"📁 找到 {len(video_files)} 个视频文件")
    print(f"\n📊 视频列表（按下载时间排序）：")
    for i, video in enumerate(video_files, 1):
        print(f"   {i}. {os.path.basename(video)}")
    
    if len(video_files) < 10:
        print(f"\n❌ 视频数量不足 10 个")
        return
    
    # 第 10 个视频（最后一个）
    target_video = video_files[9]  # 索引从 0 开始
    
    print(f"\n🎯 目标视频（第 10 个）：{os.path.basename(target_video)}")
    
    # 输出封面路径
    output_cover = "test_cover_video10.jpg"
    
    # 提取封面
    print(f"\n开始提取封面...")
    success = extract_cover_from_video(target_video, output_cover)
    
    if success:
        print(f"\n🎉 封面提取成功！")
        print(f"📁 封面位置: {os.path.abspath(output_cover)}")
        print(f"💡 你可以在文件管理器中打开查看")
    else:
        print(f"\n❌ 封面提取失败")

if __name__ == "__main__":
    test_extract_cover()
