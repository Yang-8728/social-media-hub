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
    
    def upload(self, video_path: str, category: str = "生活", subcategory: str = None) -> bool:
        """上传视频文件
        
        Args:
            video_path: 视频文件路径
            category: B站分区类别，如："生活"、"娱乐"、"科技"、"游戏"、"小剧场"等
            subcategory: 子分区，如："搞笑研究所"（当主分区为"小剧场"时）
        """
        try:
            print(f"📤 开始上传视频: {video_path}")
            print(f"🏷️ 目标分区: {category}")
            if subcategory:
                print(f"🏷️ 目标子分区: {subcategory}")
            
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

            # 选择分区
            try:
                print(f"🏷️ 尝试设置分区为: {category}")
                
                # 等待页面完全加载
                time.sleep(3)
                
                # 查找分区下拉菜单的触发器（点击展开）
                dropdown_selectors = [
                    (By.XPATH, "//div[contains(text(),'分区')]//following-sibling::*//div[contains(@class,'select')]"),
                    (By.XPATH, "//span[contains(text(),'分区')]//following-sibling::*//div[contains(@class,'select')]"),
                    (By.XPATH, "//div[contains(@class,'category')]//div[contains(@class,'select')]"),
                    (By.CSS_SELECTOR, "div[class*='category'] div[class*='select']"),
                    (By.CSS_SELECTOR, "div[class*='select']"),
                    (By.XPATH, "//div[text()='分区']/..//div[contains(@class,'select')] | //div[text()='分区']/following-sibling::*//div[contains(@class,'select')]")
                ]
                
                category_selected = False
                
                print("🔍 寻找分区下拉菜单...")
                
                for by, selector in dropdown_selectors:
                    try:
                        dropdown_elements = self.driver.find_elements(by, selector)
                        print(f"找到 {len(dropdown_elements)} 个可能的下拉菜单元素")
                        
                        for dropdown in dropdown_elements:
                            try:
                                if dropdown.is_displayed():
                                    print("🎯 找到可见的下拉菜单，尝试点击展开...")
                                    
                                    # 滚动到元素
                                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
                                    time.sleep(0.5)
                                    
                                    # 点击展开下拉菜单
                                    dropdown.click()
                                    time.sleep(1.5)
                                    
                                    # 查找展开后的选项
                                    option_selectors = [
                                        (By.XPATH, f"//div[contains(@class,'option')][contains(text(),'{category}')]"),
                                        (By.XPATH, f"//li[contains(@class,'option')][contains(text(),'{category}')]"),
                                        (By.XPATH, f"//div[contains(text(),'{category}')]"),
                                        (By.XPATH, f"//span[contains(text(),'{category}')]"),
                                        (By.XPATH, f"//*[text()='{category}']")
                                    ]
                                    
                                    option_found = False
                                    for opt_by, opt_selector in option_selectors:
                                        try:
                                            option_elements = self.driver.find_elements(opt_by, opt_selector)
                                            for option_elem in option_elements:
                                                if option_elem.is_displayed() and category in option_elem.text:
                                                    print(f"🎯 找到目标选项: {option_elem.text}")
                                                    option_elem.click()
                                                    print(f"✅ 分区已设置为: {category}")
                                                    category_selected = True
                                                    option_found = True
                                                    break
                                            if option_found:
                                                break
                                        except Exception:
                                            continue
                                    
                                    if option_found:
                                        break
                                    else:
                                        # 显示所有可用选项
                                        print("🔍 显示下拉菜单中的所有选项:")
                                        all_options = self.driver.find_elements(By.XPATH, "//div[contains(@class,'option')] | //li[contains(@class,'option')]")
                                        for opt in all_options:
                                            if opt.is_displayed() and opt.text.strip():
                                                print(f"  - {opt.text.strip()}")
                            except Exception as e:
                                print(f"处理下拉菜单失败: {e}")
                                continue
                        
                        if category_selected:
                            break
                            
                    except Exception as e:
                        continue
                
                if not category_selected:
                    print(f"⚠️ 未能成功设置分区为'{category}'，将使用默认分区")
                else:
                    # 如果成功选择了主分区，并且指定了子分区，尝试选择子分区
                    if subcategory:
                        print(f"🔍 等待子分区选项加载...")
                        time.sleep(2)  # 等待子分区选项加载
                        
                        try:
                            print(f"🏷️ 尝试选择子分区: {subcategory}")
                            
                            # 查找子分区选择器
                            subcategory_selectors = [
                                (By.XPATH, f"//div[contains(@class,'option')][contains(text(),'{subcategory}')]"),
                                (By.XPATH, f"//li[contains(@class,'option')][contains(text(),'{subcategory}')]"),
                                (By.XPATH, f"//div[contains(text(),'{subcategory}')]"),
                                (By.XPATH, f"//span[contains(text(),'{subcategory}')]"),
                                (By.XPATH, f"//*[text()='{subcategory}']"),
                                (By.XPATH, f"//div[contains(@class,'sub')]//div[contains(text(),'{subcategory}')]"),
                                (By.XPATH, f"//div[contains(@class,'category')]//div[contains(text(),'{subcategory}')]")
                            ]
                            
                            subcategory_selected = False
                            for sub_by, sub_selector in subcategory_selectors:
                                try:
                                    subcategory_elements = self.driver.find_elements(sub_by, sub_selector)
                                    for sub_elem in subcategory_elements:
                                        if sub_elem.is_displayed() and subcategory in sub_elem.text:
                                            print(f"🎯 找到子分区选项: {sub_elem.text}")
                                            
                                            # 滚动到元素
                                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sub_elem)
                                            time.sleep(0.5)
                                            
                                            # 点击选择子分区
                                            sub_elem.click()
                                            print(f"✅ 子分区已设置为: {subcategory}")
                                            subcategory_selected = True
                                            break
                                    if subcategory_selected:
                                        break
                                except Exception:
                                    continue
                            
                            if not subcategory_selected:
                                print(f"⚠️ 未找到子分区'{subcategory}'，显示页面上的所有可点击元素:")
                                # 显示所有可能的子分区选项
                                all_clickable = self.driver.find_elements(By.XPATH, "//*[contains(@class,'option') or contains(text(),'研究所') or contains(text(),'剧场')]")
                                for elem in all_clickable:
                                    if elem.is_displayed() and elem.text.strip():
                                        print(f"  - {elem.text.strip()}")
                                        
                        except Exception as e:
                            print(f"⚠️ 子分区设置过程出错: {e}")
                    
            except Exception as e:
                print(f"⚠️ 分区设置过程出错: {e}")
                print("将使用系统默认分区")

            # 无论分区是否成功，都继续执行投稿流程
            print("📋 分区设置完成，继续投稿流程...")
            
            # 尝试自动点击“立即投稿/发布/提交”按钮
            try:
                print("🔍 寻找并点击“立即投稿/发布/提交”按钮...")
                clicked = False
                # 先滚动到页面底部，因为立即投稿按钮在最下面
                print("⬇️ 滚动到页面底部寻找投稿按钮...")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                submit_selectors = [
                    # 根据原项目的选择器 - 关键是用span标签
                    (By.XPATH, '//span[contains(text(), "立即投稿")]'),
                    (By.XPATH, "//span[text()='立即投稿']"),
                    (By.XPATH, "//span[normalize-space(.)='立即投稿']"),
                    # 备选按钮选择器
                    (By.XPATH, "//button[contains(text(), '立即投稿')]"),
                    (By.XPATH, "//button[text()='立即投稿']"),
                    (By.XPATH, "//button[normalize-space(.)='立即投稿']"),
                    # 作为最后备选，查找所有span和button然后筛选
                    (By.TAG_NAME, "span"),
                    (By.TAG_NAME, "button")
                ]

                # 轮询等待可点击
                end_time = time.time() + 30
                while time.time() < end_time and not clicked:
                    for by, sel in submit_selectors:
                        try:
                            buttons = self.driver.find_elements(by, sel)
                            print(f"找到 {len(buttons)} 个可能的投稿按钮")
                            
                            for btn in buttons:
                                try:
                                    if btn.is_displayed() and btn.is_enabled():
                                        button_text = btn.text.strip()
                                        button_class = btn.get_attribute('class')
                                        print(f"🔍 检查元素: '{button_text}' (tag: {btn.tag_name}, class: {button_class})")
                                        
                                        # 专门匹配"立即投稿"，支持span和button标签
                                        if button_text == '立即投稿':
                                            print(f"🎯 找到立即投稿元素: '{button_text}' (tag: {btn.tag_name})")
                                            
                                            # 滚动到元素位置
                                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                                            time.sleep(0.5)
                                            
                                            try:
                                                # 参考原项目，使用ActionChains点击
                                                from selenium.webdriver.common.action_chains import ActionChains
                                                ActionChains(self.driver).move_to_element(btn).pause(0.5).click().perform()
                                                print(f"✅ 已点击立即投稿(ActionChains): '{button_text}'")
                                                clicked = True
                                                break
                                            except Exception:
                                                # 如果ActionChains失败，尝试普通点击
                                                try:
                                                    btn.click()
                                                    print(f"✅ 已点击立即投稿(click): '{button_text}'")
                                                    clicked = True
                                                    break
                                                except Exception:
                                                    # 最后尝试JavaScript点击
                                                    self.driver.execute_script("arguments[0].click();", btn)
                                                    print(f"✅ 已点击立即投稿(JS): '{button_text}'")
                                                    clicked = True
                                                    break
                                        # 如果不是"立即投稿"，跳过其他元素
                                        elif button_text in ['添加分P', '添加分p', '选择文件', '上传', '浏览']:
                                            print(f"⚠️ 跳过元素: '{button_text}' (不是目标元素)")
                                            continue
                                except Exception as e:
                                    continue
                            
                            if clicked:
                                break
                                
                        except Exception:
                            continue
                    
                    if not clicked:
                        time.sleep(1)
                
                # 如果还是没找到，显示页面底部的所有按钮供调试
                if not clicked:
                    print("🔍 显示页面底部的所有按钮:")
                    all_buttons = self.driver.find_elements(By.XPATH, "//button")
                    for i, btn in enumerate(all_buttons[-10:]):  # 只显示最后10个按钮
                        try:
                            if btn.is_displayed():
                                btn_text = btn.text.strip()
                                btn_class = btn.get_attribute('class')
                                print(f"  按钮 {i+1}: '{btn_text}' (class: {btn_class})")
                        except:
                            continue

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
