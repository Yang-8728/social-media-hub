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
            
            # 尝试自动点击“立即投稿/发布/提交”按钮
            try:
                print("🔍 寻找并点击“立即投稿/发布/提交”按钮...")
                clicked = False
                submit_selectors = [
                    (By.XPATH, "//button[.//span[contains(text(),'立即投稿')] or contains(normalize-space(.), '立即投稿')]") ,
                    (By.XPATH, "//button[contains(normalize-space(.), '发布')]"),
                    (By.XPATH, "//button[contains(normalize-space(.), '提交')]"),
                    (By.XPATH, "//button[contains(normalize-space(.), '投稿')]")
                ]

                # 轮询等待可点击
                end_time = time.time() + 30
                while time.time() < end_time and not clicked:
                    for by, sel in submit_selectors:
                        try:
                            btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((by, sel)))
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                            time.sleep(0.2)
                            try:
                                btn.click()
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", btn)
                            print("✅ 已点击提交按钮")
                            clicked = True
                            break
                        except Exception:
                            continue
                    if not clicked:
                        time.sleep(1)

                # 若有确认弹窗，尝试点击“确定/确认/继续”
                if clicked:
                    try:
                        confirm = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[contains(normalize-space(.), '确定') or contains(normalize-space(.), '确认') or contains(normalize-space(.), '继续') or contains(normalize-space(.), '我知道了')]"
                        )))
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm)
                        time.sleep(0.2)
                        try:
                            confirm.click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", confirm)
                        print("✅ 已点击确认按钮")
                    except Exception:
                        pass

                    # 等待跳转或成功提示
                    try:
                        WebDriverWait(self.driver, 20).until(
                            EC.any_of(
                                EC.url_contains("manage"),
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'投稿成功') or contains(text(),'发布成功') or contains(text(),'提交成功')]") )
                            )
                        )
                        print("� 投稿流程已提交（检测到成功信号或页面跳转）")
                    except Exception:
                        print("⚠️ 未检测到成功信号，可能仍需人工补充必填项")
                else:
                    print("⚠️ 未找到可点击的投稿按钮，可能尚未满足必填项或页面布局变化")
            except Exception as e:
                print(f"⚠️ 自动点击投稿按钮过程出错: {e}")

            print("✅ 上传流程结束。将短暂停留供你检查，随后自动关闭浏览器...")
            time.sleep(8)
            
            return True
            
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
