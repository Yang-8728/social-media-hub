#!/usr/bin/env python3
"""
测试B站上传器原始配置文件
"""
from src.platforms.bilibili.uploader import BilibiliUploader
import time

def test_original_profile():
    """测试使用原始配置文件的上传器"""
    print('=== 测试原始配置文件的B站上传器 ===')
    
    try:
        uploader = BilibiliUploader('ai_vanvan')
        print(f'配置文件路径: {uploader.profile_path}')
        
        driver, wait = uploader._init_browser()
        print('✅ 浏览器初始化成功!')
        
        print('🌐 导航到B站...')
        driver.get('https://www.bilibili.com')
        time.sleep(8)
        
        print(f'📄 页面标题: {driver.title}')
        
        # 检查登录状态
        page_source = driver.page_source
        if '登录' in page_source and ('用户中心' not in page_source and '个人中心' not in page_source):
            print('❌ 仍为未登录状态')
        elif '用户中心' in page_source or '个人中心' in page_source or '投稿' in page_source:
            print('✅ 已登录状态 - 检测到用户功能')
        else:
            print('⚠️ 登录状态不明确，让我们检查页面内容...')
            # 检查是否有用户名或头像
            if 'avatar' in page_source.lower() or '头像' in page_source:
                print('✅ 可能已登录 - 检测到头像元素')
            else:
                print('❌ 可能未登录')
        
        print('🔍 保持浏览器开启15秒供检查...')
        time.sleep(15)
        driver.quit()
        print('✅ 测试完成')
        
        return True
        
    except Exception as e:
        print(f'❌ 测试失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_original_profile()
