#!/usr/bin/env python3
"""
B站上传功能实际测试
Real Bilibili Upload Test
"""
import os
import sys
import time

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata


def find_latest_merged_video():
    """查找最新的合并视频"""
    merged_folders = [
        os.path.join(project_root, "data", "merged"),
        os.path.join("c:", "Code", "insDownloader", "merged"),
        os.path.join(project_root, "data", "merged", "ai_vanvan")
    ]
    
    videos = []
    for folder in merged_folders:
        if os.path.exists(folder):
            import glob
            folder_videos = glob.glob(os.path.join(folder, "*.mp4"))
            videos.extend(folder_videos)
    
    if not videos:
        return None
    
    # 返回最新的视频
    return max(videos, key=os.path.getmtime)


def create_demo_video():
    """创建一个演示视频"""
    demo_path = os.path.join(project_root, "temp", "demo_video.mp4")
    os.makedirs(os.path.dirname(demo_path), exist_ok=True)
    
    # 创建一个大一点的假视频文件（1MB）
    with open(demo_path, 'wb') as f:
        f.write(b"0" * 1024 * 1024)  # 1MB的假数据
    
    return demo_path


def test_real_upload():
    """实际上传测试"""
    print("=" * 60)
    print("🚀 B站上传功能实际测试")
    print("=" * 60)
    
    # 查找视频文件
    video_path = find_latest_merged_video()
    
    if not video_path:
        print("⚠️  未找到合并视频，创建演示视频...")
        video_path = create_demo_video()
        print(f"演示视频创建: {video_path}")
    else:
        print(f"找到视频文件: {os.path.basename(video_path)}")
        print(f"完整路径: {video_path}")
        
        # 显示文件信息
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        mod_time = time.strftime('%Y-%m-%d %H:%M:%S', 
                                time.localtime(os.path.getmtime(video_path)))
        print(f"文件大小: {file_size:.1f} MB")
        print(f"修改时间: {mod_time}")
    
    print("\n" + "=" * 60)
    print("账号选择:")
    print("1. ai_vanvan (海外离大谱#)")
    print("2. aigf8728 (AIGF#)")
    print("3. 退出")
    
    choice = input("\n请选择账号 (1-3): ").strip()
    
    if choice == "3":
        print("👋 退出测试")
        return
    
    account_name = "ai_vanvan" if choice == "1" else "aigf8728"
    print(f"\n选择账号: {account_name}")
    
    # 创建上传器
    print("\n" + "=" * 60)
    print("初始化上传器...")
    uploader = BilibiliUploader(account_name)
    
    # 创建元数据
    metadata = VideoMetadata(
        title="测试上传",
        description="这是一个测试上传的视频",
        tags=["测试", "上传", "B站"]
    )
    
    print(f"上传账号: {account_name}")
    print(f"视频文件: {os.path.basename(video_path)}")
    print(f"Chrome配置: {uploader.profile_path}")
    
    # 确认上传
    print("\n" + "=" * 60)
    print("⚠️  注意：这将打开浏览器并尝试上传视频到B站")
    print("请确保:")
    print("1. 你已经在Chrome中登录了对应的B站账号")
    print("2. 网络连接正常")
    print("3. 有足够时间完成上传流程")
    
    confirm = input("\n确认继续上传？(y/n): ").strip().lower()
    
    if confirm != 'y':
        print("👋 取消上传")
        # 清理演示文件
        if video_path.endswith("demo_video.mp4"):
            os.remove(video_path)
        return
    
    # 开始上传
    print("\n" + "=" * 60)
    print("🚀 开始上传...")
    print("请在浏览器中完成登录（如需要）...")
    
    try:
        result = uploader.upload(video_path, metadata)
        
        print("\n" + "=" * 60)
        print("📊 上传结果:")
        print("=" * 60)
        print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
        print(f"平台: {result.platform}")
        print(f"账号: {result.account}")
        print(f"用时: {int(result.duration)} 秒")
        print(f"消息: {result.message}")
        
        if result.error:
            print(f"错误: {result.error}")
        
        if result.success:
            print("\n🎉 上传成功！")
            print("可以去B站检查视频是否正确上传")
        else:
            print("\n❌ 上传失败，请检查错误信息")
            
    except KeyboardInterrupt:
        print("\n⏹️  用户中断上传")
    except Exception as e:
        print(f"\n❌ 上传过程发生异常: {e}")
    finally:
        # 清理演示文件
        if video_path.endswith("demo_video.mp4") and os.path.exists(video_path):
            os.remove(video_path)
            print("\n🗑️  清理演示文件")


def test_browser_only():
    """仅测试浏览器打开（不上传）"""
    print("=" * 60)
    print("🔧 浏览器测试模式")
    print("=" * 60)
    
    account_name = "ai_vanvan"
    uploader = BilibiliUploader(account_name)
    
    print(f"账号: {account_name}")
    print(f"Chrome路径: {uploader.chrome_path}")
    print(f"配置文件: {uploader.profile_path}")
    
    try:
        print("\n正在初始化浏览器...")
        driver, wait = uploader._init_browser()
        
        print("✅ 浏览器初始化成功")
        print("正在打开B站投稿页面...")
        
        driver.get("https://member.bilibili.com/platform/upload/video/")
        print("✅ 投稿页面已打开")
        print("请在浏览器中检查页面是否正常加载")
        
        input("\n按回车键关闭浏览器...")
        driver.quit()
        print("✅ 浏览器已关闭")
        
    except Exception as e:
        print(f"❌ 浏览器测试失败: {e}")


def main():
    """主菜单"""
    while True:
        print("\n" + "=" * 60)
        print("🚀 B站上传功能测试")
        print("=" * 60)
        print("1. 实际上传测试")
        print("2. 浏览器测试（仅打开页面）")
        print("3. 退出")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            test_real_upload()
        elif choice == "2":
            test_browser_only()
        elif choice == "3":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    main()
