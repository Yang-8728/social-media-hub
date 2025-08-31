#!/usr/bin/env python3
"""
测试上传功能
Test Upload Functionality
"""
import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata


def test_uploader_init():
    """测试上传器初始化"""
    print("=== 测试上传器初始化 ===")
    try:
        uploader = BilibiliUploader("ai_vanvan")
        print(f"✅ 上传器初始化成功")
        print(f"   账号名称: {uploader.account_name}")
        print(f"   Chrome路径: {uploader.chrome_path}")
        print(f"   ChromeDriver路径: {uploader.chromedriver_path}")
        print(f"   配置文件路径: {uploader.profile_path}")
        print(f"   截图目录: {uploader.screenshot_dir}")
        return True
    except Exception as e:
        print(f"❌ 上传器初始化失败: {e}")
        return False


def test_browser_init():
    """测试浏览器初始化"""
    print("\n=== 测试浏览器初始化 ===")
    try:
        uploader = BilibiliUploader("ai_vanvan")
        
        # 检查Chrome文件是否存在
        if not os.path.exists(uploader.chrome_path):
            print(f"❌ Chrome浏览器不存在: {uploader.chrome_path}")
            return False
        
        if not os.path.exists(uploader.chromedriver_path):
            print(f"❌ ChromeDriver不存在: {uploader.chromedriver_path}")
            return False
        
        print(f"✅ Chrome工具文件检查通过")
        print(f"   Chrome浏览器: 存在")
        print(f"   ChromeDriver: 存在")
        
        # 尝试初始化浏览器（但不执行实际操作）
        print("⚠️  浏览器初始化需要在实际上传时测试")
        return True
        
    except Exception as e:
        print(f"❌ 浏览器初始化测试失败: {e}")
        return False


def test_account_config():
    """测试账号配置"""
    print("\n=== 测试账号配置 ===")
    try:
        from src.accounts.config import AccountManager
        
        account_manager = AccountManager()
        accounts = account_manager.list_accounts()
        
        print(f"✅ 账号管理器初始化成功")
        print(f"   可用账号: {accounts}")
        
        for account_name in accounts:
            config = account_manager.get_account_config(account_name)
            print(f"\n   账号: {account_name}")
            print(f"     平台: {config.platform}")
            print(f"     标题前缀: {config.title_prefix}")
            print(f"     序列号文件: {config.serial_number_file}")
            print(f"     Chrome配置: {config.chrome_profile_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 账号配置测试失败: {e}")
        return False


def create_test_video():
    """创建一个测试视频文件"""
    test_video_path = os.path.join(project_root, "temp", "test_video.mp4")
    os.makedirs(os.path.dirname(test_video_path), exist_ok=True)
    
    # 创建一个小的测试文件（模拟视频）
    with open(test_video_path, 'wb') as f:
        f.write(b"fake video content for testing")
    
    return test_video_path


def test_dry_run():
    """测试上传功能（干运行）"""
    print("\n=== 测试上传功能（干运行）===")
    try:
        # 创建测试视频
        test_video = create_test_video()
        print(f"创建测试视频: {test_video}")
        
        # 创建上传器
        uploader = BilibiliUploader("ai_vanvan")
        
        # 创建视频元数据
        metadata = VideoMetadata(
            title="测试视频",
            description="这是一个测试视频",
            tags=["测试", "demo"]
        )
        
        print(f"✅ 上传功能测试准备完成")
        print(f"   测试视频: {os.path.basename(test_video)}")
        print(f"   上传账号: {uploader.account_name}")
        print(f"   ⚠️  实际上传需要手动执行")
        
        # 清理测试文件
        if os.path.exists(test_video):
            os.remove(test_video)
        
        return True
        
    except Exception as e:
        print(f"❌ 上传功能测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试上传功能...")
    
    tests = [
        ("上传器初始化", test_uploader_init),
        ("浏览器初始化", test_browser_init),
        ("账号配置", test_account_config),
        ("上传功能", test_dry_run)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ 测试 '{test_name}' 发生异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "="*50)
    print("📊 测试结果汇总:")
    print("="*50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("\n🎉 所有测试通过！上传功能基础设施准备就绪")
        print("\n下一步:")
        print("   1. 运行实际上传测试")
        print("   2. 配置账号登录信息")
        print("   3. 测试完整上传流程")
    else:
        print(f"\n⚠️  有 {len(results) - passed} 个测试失败，请检查配置")


if __name__ == "__main__":
    main()
