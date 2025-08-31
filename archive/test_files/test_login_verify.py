#!/usr/bin/env python3
"""
验证B站登录状态保存情况
"""
from src.platforms.bilibili.uploader import BilibiliUploader
import time

def verify_login_status():
    """验证登录状态是否已保存"""
    print('=== 验证登录状态保存情况 ===')
    
    try:
        uploader = BilibiliUploader('ai_vanvan')
        driver, wait = uploader._init_browser()
        print('✅ 浏览器启动成功')
        
        driver.get('https://www.bilibili.com')
        time.sleep(5)
        print(f'📄 页面标题: {driver.title}')

        # 更准确的登录检测
        page_source = driver.page_source
        
        if '扫码登录' in page_source:
            print('❌ 显示扫码登录界面，未保持登录状态')
        elif '登录' in page_source and not any(x in page_source for x in ['投稿', '用户中心', '个人中心', '私信']):
            print('❌ 仍显示登录按钮，未保持登录状态')
        else:
            print('✅ 登录状态已保存！没有看到登录界面')
            if any(x in page_source for x in ['投稿', '用户中心', '个人中心', '私信', 'avatar']):
                print('✅ 确认：检测到已登录用户功能')

        print('⏰ 保持浏览器开启10秒供确认...')
        time.sleep(10)
        driver.quit()
        print('✅ 验证完成')
        
        return True
        
    except Exception as e:
        print(f'❌ 验证失败: {e}')
        return False

if __name__ == "__main__":
    verify_login_status()
