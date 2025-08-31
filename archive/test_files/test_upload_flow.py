#!/usr/bin/env python3
"""
测试B站上传功能 - 基础上传流程
"""
from src.platforms.bilibili.uploader import BilibiliUploader
from src.core.models import VideoMetadata
import time
import os

def test_upload_flow():
    """测试上传功能流程"""
    print('=== 测试B站上传功能流程 ===')
    
    try:
        uploader = BilibiliUploader('ai_vanvan')
        driver, wait = uploader._init_browser()
        print('✅ 浏览器启动成功')
        
        # 导航到创作中心
        print('🚀 导航到B站创作中心...')
        driver.get('https://member.bilibili.com/york/videoup')
        time.sleep(5)
        
        print(f'📄 当前页面: {driver.title}')
        
        # 检查是否成功进入投稿页面
        page_source = driver.page_source
        if '视频投稿' in page_source or '上传视频' in page_source or 'videoup' in driver.current_url:
            print('✅ 成功进入视频投稿页面')
            
            # 查找上传按钮或拖拽区域
            if '点击上传' in page_source or '拖拽到此区域' in page_source or 'upload' in page_source:
                print('✅ 找到视频上传区域')
            else:
                print('⚠️ 未找到明显的上传区域，但页面已加载')
                
        else:
            print('❌ 未能进入投稿页面，可能需要额外权限')
        
        print('🔍 保持页面开启15秒供检查上传界面...')
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
    test_upload_flow()
