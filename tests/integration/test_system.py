"""
测试脚本 - 验证完整的下载和合并流程
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import Logger
from src.utils.video_merger import VideoMerger


def test_logger():
    """测试日志功能"""
    print("=== 测试日志功能 ===")
    
    logger = Logger("test_account")
    
    # 模拟记录一些下载
    logger.record_download("shortcode1", "success", "path/to/video1.mp4")
    logger.record_download("shortcode2", "success", "path/to/video2.mp4")
    logger.record_download("shortcode3", "failed", error="网络错误")
    logger.record_download("shortcode4", "skipped", "path/to/video4.mp4")
    
    # 显示汇总
    summary = logger.get_download_summary()
    print("下载汇总:", summary)
    
    # 显示未合并的
    unmerged = logger.get_unmerged_downloads()
    print("未合并列表:", unmerged)
    
    # 标记一个为已合并
    if unmerged:
        logger.mark_as_merged(unmerged[0], "path/to/merged1.mp4")
        print(f"标记 {unmerged[0]} 为已合并")
    
    # 再次检查
    unmerged_after = logger.get_unmerged_downloads()
    print("合并后未合并列表:", unmerged_after)
    
    print("✅ 日志功能测试完成\n")


def test_video_merger():
    """测试视频合并器"""
    print("=== 测试视频合并器 ===")
    
    merger = VideoMerger("test_account")
    
    # 检查 ffmpeg
    if merger.ffmpeg_path:
        print(f"✅ 找到 ffmpeg: {merger.ffmpeg_path}")
    else:
        print("⚠️  未找到 ffmpeg，某些功能将不可用")
    
    # 测试获取已合并的视频
    merged_videos = merger.get_merged_videos()
    print(f"已合并的视频数量: {len(merged_videos)}")
    
    print("✅ 视频合并器测试完成\n")


def test_directory_structure():
    """测试目录结构"""
    print("=== 检查目录结构 ===")
    
    required_dirs = [
        "data",
        "data/downloads",
        "data/merged",
        "logs",
        "temp"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} 存在")
        else:
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 创建目录: {dir_path}")
    
    print("✅ 目录结构检查完成\n")


def show_usage_examples():
    """显示使用示例"""
    print("=== 使用示例 ===")
    print("1. 下载内容:")
    print("   python main.py --download --vanvan --limit 5")
    print("   python main.py --download --aigf --limit 3")
    print("   python main.py --download --all --limit 2")
    print("")
    print("2. 合并视频:")
    print("   python main.py --merge --vanvan")
    print("   python main.py --merge --all")
    print("")
    print("3. 查看状态:")
    print("   python main.py --status")
    print("   python main.py --status --account ai_vanvan")
    print("")
    print("4. 完整流程:")
    print("   python main.py --download --vanvan --limit 5")
    print("   python main.py --merge --vanvan")
    print("   python main.py --status --vanvan")
    print("")


def main():
    """主测试函数"""
    print("🧪 Social Media Hub 系统测试")
    print("=" * 50)
    
    test_directory_structure()
    test_logger()
    test_video_merger()
    show_usage_examples()
    
    print("🎉 所有测试完成！")
    print("")
    print("📋 现在你可以:")
    print("1. 确保 Firefox 已登录 Instagram")
    print("2. 运行下载命令测试实际下载")
    print("3. 运行合并命令处理下载的视频")
    print("4. 使用 --status 查看下载和合并状态")


if __name__ == "__main__":
    main()
