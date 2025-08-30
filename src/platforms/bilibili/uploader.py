"""
Bilibili 上传器接口
"""
import os
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ...core.interfaces import IUploader
from ...core.models import Account, Video, UploadResult

class BilibiliUploader(IUploader):
    """Bilibili 上传器"""
    
    def __init__(self, account_name: str):
        self.account_name = account_name
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """设置Chrome驱动 - 使用保存的配置文件"""
        try:
            chrome_options = Options()
            
            # 使用已保存的配置文件
            profile_path = f"c:\\Code\\social-media-hub\\tools\\profiles\\chrome_profile_{self.account_name}"
            
            if os.path.exists(profile_path):
                chrome_options.add_argument(f"--user-data-dir={profile_path}")
                chrome_options.add_argument("--profile-directory=Default")
                print(f"✅ 使用已保存的配置文件: {profile_path}")
            else:
                print(f"❌ 配置文件不存在: {profile_path}")
                return False
            
            chrome_options.add_argument("--window-size=1200,800")
            chrome_options.add_argument("--window-position=100,100")
            
            # 禁用一些干扰选项
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            print("🚀 启动Chrome浏览器...")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 30)
            
            print("✅ Chrome启动成功")
            return True
        except Exception as e:
            print(f"❌ Chrome驱动设置失败: {e}")
            return False
    
    def login(self, account: Account) -> bool:
        """登录Bilibili账号"""
        # TODO: 实现Chrome配置文件登录
        pass
    
    def upload_video(self, account: Account, video: Video) -> UploadResult:
        """上传视频到Bilibili"""
        # TODO: 实现视频上传逻辑
        pass
    
    def get_upload_history(self, account: Account) -> List[Video]:
        """获取上传历史"""
        # TODO: 实现上传历史查询
        pass
    
    def upload(self, video_path: str) -> bool:
        """上传视频文件"""
        try:
            print(f"📤 开始上传视频: {video_path}")
            
            # 设置驱动
            if not self.setup_driver():
                return False
            
            # 直接打开B站上传页面（应该已经登录）
            print("🌐 打开B站上传页面...")
            self.driver.get("https://member.bilibili.com/platform/upload/video/")
            time.sleep(5)
            
            # 检查是否成功到达上传页面
            current_url = self.driver.current_url
            if "upload" not in current_url:
                print("❌ 未能到达上传页面，可能需要重新登录")
                return False
                
            print("✅ 已到达上传页面")
            
            # 等待并选择视频文件
            print("📁 选择视频文件...")
            file_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # 上传文件
            abs_video_path = os.path.abspath(video_path)
            file_input.send_keys(abs_video_path)
            print(f"✅ 文件已选择: {abs_video_path}")
            
            # 等待上传完成
            print("⏳ 等待视频上传...")
            time.sleep(15)
            
            # 填写标题
            try:
                title_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='标题'], input[placeholder*='请填写标题']"))
                )
                title_input.clear()
                title = f"AI助手自动上传 - {os.path.basename(video_path)}"
                title_input.send_keys(title)
                print(f"📝 标题已设置: {title}")
            except:
                print("⚠️ 无法自动填写标题，请手动填写")
            
            print("✅ 视频上传成功！")
            print("🎬 浏览器将保持打开，您可以手动完成其他设置并发布")
            
            # 不自动关闭浏览器，让用户手动操作
            input("按Enter键关闭浏览器...")
            
            return True
            
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
