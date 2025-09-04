"""
Bilibili 上传器接口 - 优化版本
"""
import os
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from ...core.interfaces import IUploader
from ...core.models import Account, Video, UploadResult

class BilibiliUploader(IUploader):
    """Bilibili 上传器 - 优化版本"""
    
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
            
            # 窗口设置
            chrome_options.add_argument("--window-size=1200,800")
            chrome_options.add_argument("--window-position=100,100")
            
            # 稳定性选项 - 修复启动崩溃问题
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            
            # 禁用自动化检测
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 抑制Chrome日志和错误输出
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent") 
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            print("🚀 启动Chrome浏览器...")
            
            # 设置ChromeDriver服务，增加超时时间
            from selenium.webdriver.chrome.service import Service
            service = Service()
            service.start_timeout = 60  # 增加启动超时时间
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 30)
            
            print("✅ Chrome启动成功")
            return True
        except Exception as e:
            print(f"❌ Chrome驱动设置失败: {e}")
            print("💡 尝试备用启动方案...")
            return self._try_fallback_driver()
            
    def _try_fallback_driver(self):
        """备用Chrome启动方案 - 不使用配置文件"""
        try:
            chrome_options = Options()
            
            # 基础稳定性设置
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1200,800")
            chrome_options.add_argument("--remote-debugging-port=9223")  # 使用不同端口
            
            print("� 尝试不使用配置文件启动Chrome...")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 30)
            
            print("✅ Chrome备用方案启动成功")
            print("⚠️ 注意：未使用保存的登录状态，需要手动登录")
            return True
        except Exception as e:
            print(f"❌ 备用启动方案也失败: {e}")
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
        """优化的上传视频文件方法
        
        Args:
            video_path: 视频文件路径
            category: B站分区类别，如："生活"、"娱乐"、"科技"、"游戏"、"小剧场"等
            subcategory: 子分区，如："搞笑研究所"（当主分区为"小剧场"时）
        """
        try:
            print(f"📤 开始上传视频: {video_path}")
            
            # 根据账户显示不同的分区信息
            if self.account_name == "aigf8728":
                print("🏷️ 分区: 手动选择（跳过自动设置）")
            else:
                print(f"🏷️ 目标分区: {category}")
                if subcategory:
                    print(f"🏷️ 目标子分区: {subcategory}")
            
            # 设置驱动
            if not self.setup_driver():
                if self.account_name == "aigf8728":
                    print("🔒 aigf8728账户：Chrome启动失败，但会尝试保持浏览器状态")
                    # 即使启动失败，也不立即返回False，让程序继续尝试
                    print("💡 请手动检查Chrome配置或重新尝试")
                return False
            
            # 直接打开B站上传页面（应该已经登录）
            print("🌐 正在导航到B站上传页面...")
            print("📋 目标地址: https://member.bilibili.com/platform/upload/video/frame")
            
            try:
                self.driver.get("https://member.bilibili.com/platform/upload/video/frame")
                print("✅ 页面请求已发送，等待加载...")
                time.sleep(3)
                
                # 检查当前URL
                current_url = self.driver.current_url
                print(f"📍 当前页面: {current_url}")
                
                # 等待页面完全加载
                print("⏳ 等待页面完全加载（最多30秒）...")
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                
                # 等待页面加载完成的多种信号
                try:
                    # 尝试等待上传相关元素
                    WebDriverWait(self.driver, 30).until(
                        lambda driver: "upload" in driver.current_url.lower() or 
                                     "videoup" in driver.current_url.lower() or
                                     "login" in driver.current_url.lower() or
                                     driver.find_elements(By.CSS_SELECTOR, "input[type='file']") or
                                     driver.find_elements(By.XPATH, "//*[contains(text(), '登录')]")
                    )
                    print("✅ 页面加载完成")
                except Exception as e:
                    print(f"⚠️ 页面加载超时: {e}")
                    print(f"📍 最终停留页面: {self.driver.current_url}")
                
            except Exception as e:
                print(f"❌ 导航失败: {e}")
                current_url = "未知"
            
            # 重新检查当前URL
            try:
                current_url = self.driver.current_url
                print(f"🔍 导航结果检查: {current_url}")
            except:
                current_url = "无法获取"
                
            if "upload" not in current_url.lower() and "videoup" not in current_url.lower():
                print("❌ 未能到达上传页面，可能需要重新登录")
                
                # 根据账户决定是否保持浏览器打开
                if self.account_name == "aigf8728":
                    print("🔒 aigf8728账户：浏览器保持打开状态，请手动登录并重试")
                    print("💡 请在浏览器中登录后手动导航到上传页面")
                    print("📋 上传页面地址: https://member.bilibili.com/platform/upload/video/frame")
                    # 不关闭浏览器，返回False表示需要手动操作
                    return False
                else:
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
            print("📤 视频开始上传，同时设置其他信息...")
            
            # 等待页面基本元素加载，然后并行处理
            time.sleep(3)
            
            # 1. 填写标题（快速处理）
            self._set_title(video_path)
            
            # 2. 根据账户决定是否设置分区
            if self.account_name == "aigf8728":
                print("ℹ️ aigf8728账户跳过分区设置，请在页面手动选择分区")
            else:
                # ai_vanvan等其他账户自动设置分区
                self._set_category_fast(category, subcategory)
            
            # 3. 等待并点击立即投稿
            return self._submit_and_wait_success()
            
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            
            # 判断是否为登录相关问题
            is_login_issue = False
            if hasattr(self, 'driver') and self.driver:
                try:
                    current_url = self.driver.current_url
                    if "login" in current_url or "upload" not in current_url:
                        is_login_issue = True
                except:
                    pass
            
            # 根据账户和错误类型决定是否关闭浏览器
            if self.account_name == "aigf8728" and is_login_issue:
                print("🔒 aigf8728账户：检测到登录问题，浏览器保持打开状态，请手动登录")
                print("💡 请在浏览器中登录后重新尝试上传")
            else:
                print("关闭浏览器...")
                if hasattr(self, 'driver') and self.driver:
                    self.driver.quit()
            return False
    
    def _set_title(self, video_path: str):
        """智能设置标题 - 使用ins海外利大谱#序号格式"""
        try:
            title_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='标题'], input[placeholder*='请填写标题']"))
            )
            
            # 强力清空输入框
            title_input.clear()
            title_input.send_keys(Keys.CONTROL + "a")  # 全选
            title_input.send_keys(Keys.DELETE)  # 删除
            
            # 生成正确的标题格式（但不立即增加序号）
            title = self._generate_title_preview(video_path)
            title_input.send_keys(title)
            print(f"📝 标题已设置: {title}")
            
            # 保存当前使用的序号（用于失败时回退）
            self.current_episode_number = self._get_current_episode_number()
        except:
            print("⚠️ 无法自动填写标题，请手动填写")
    
    def _generate_title_preview(self, video_path: str = None) -> str:
        """生成标题预览 - 根据账户配置生成不同格式"""
        try:
            # 获取当前序号（不增加）
            current_number = self._get_current_episode_number()
            
            # 根据账户名生成不同的标题格式
            if self.account_name == "aigf8728":
                # 尝试从视频路径提取博主ID
                blogger_id = self._extract_blogger_id(video_path) if video_path else "[博主ID]"
                print(f"🔍 调试信息 - 视频路径: {video_path}")
                print(f"🔍 调试信息 - 提取的博主ID: '{blogger_id}'")
                print(f"🔍 调试信息 - 当前序号: {current_number}")
                
                title = f"ins你的海外第{current_number}个女友:{blogger_id}"
                print(f"🔍 调试信息 - 生成的标题: '{title}'")
            else:
                # 默认 ai_vanvan 格式
                title = f"ins海外离大谱#{current_number}"
            
            return title
        except Exception as e:
            print(f"⚠️ 生成标题失败: {e}")
            # 如果获取序号失败，使用默认格式
            if self.account_name == "aigf8728":
                return "ins你的海外第6个女友:[博主ID]"
            else:
                return "ins海外离大谱#84"
    
    def _extract_blogger_id(self, video_path: str) -> str:
        """从视频路径中提取博主ID"""
        if not video_path:
            return "[博主ID]"
        
        try:
            import os
            
            # 如果是合并后的视频（在merged文件夹中），需要从合并日志中查找原始视频信息
            if "merged" in video_path.lower():
                return self._extract_blogger_from_merged_video(video_path)
            
            # 如果是原始视频，直接从路径提取
            # aigf8728 使用 date_blogger 策略，路径格式如：
            # .../downloads/aigf8728/2025-09-04_blogger_name/video.mp4
            path_parts = os.path.normpath(video_path).split(os.sep)
            
            # 找到包含日期_博主ID的文件夹
            for part in path_parts:
                if '_' in part and len(part.split('_')[0]) == 10:  # 检查是否是日期格式 YYYY-MM-DD
                    date_blogger = part.split('_', 1)  # 按第一个下划线分割
                    if len(date_blogger) > 1:
                        return date_blogger[1]  # 返回博主ID部分
            
            return "[博主ID]"
        except Exception as e:
            print(f"⚠️ 提取博主ID失败: {e}")
            return "[博主ID]"
    
    def _extract_blogger_from_merged_video(self, merged_video_path: str) -> str:
        """从合并视频的文件名或目录中提取博主ID"""
        try:
            import os
            
            # 首先尝试从新格式的文件名中提取
            video_filename = os.path.basename(merged_video_path).replace('.mp4', '')
            
            # 新格式：ins你的海外第N个女友_博主ID
            if "ins你的海外第" in video_filename and "个女友_" in video_filename:
                parts = video_filename.split("个女友_")
                if len(parts) > 1:
                    return parts[1]  # 返回博主ID部分
            
            # 如果文件名无法提取，从今天的下载目录中查找
            base_download_dir = f"c:\\Code\\social-media-hub\\videos\\downloads\\{self.account_name}"
            
            if not os.path.exists(base_download_dir):
                return "[博主ID]"
            
            # 遍历今天的下载文件夹，查找包含视频的博主文件夹
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            bloggers = []
            for folder in os.listdir(base_download_dir):
                if folder.startswith(today + "_") and os.path.isdir(os.path.join(base_download_dir, folder)):
                    # 提取博主ID
                    blogger_id = folder.split('_', 1)[1] if '_' in folder else folder
                    bloggers.append(blogger_id)
            
            # 如果找到博主，返回第一个（主要博主）
            if bloggers:
                # 优先返回非 "unknown" 的博主
                for blogger in bloggers:
                    if blogger != "unknown":
                        return blogger
                return bloggers[0]
            
            return "[博主ID]"
            
        except Exception as e:
            print(f"⚠️ 从合并视频提取博主ID失败: {e}")
            return "[博主ID]"
    
    def _get_current_episode_number(self) -> int:
        """获取当前集数序号（不增加）"""
        try:
            # 按账号分开管理序号文件
            sequence_file = f"logs/episodes/{self.account_name}_episode.txt"
            if os.path.exists(sequence_file):
                with open(sequence_file, 'r', encoding='utf-8') as f:
                    current_number = int(f.read().strip())
                return current_number
            else:
                # 如果文件不存在，尝试从配置文件读取起始序号
                try:
                    import json
                    config_path = "config/accounts.json"
                    with open(config_path, 'r', encoding='utf-8') as f:
                        accounts_config = json.load(f)
                    
                    if self.account_name in accounts_config:
                        account_config = accounts_config[self.account_name]
                        if 'upload' in account_config and 'next_number' in account_config['upload']:
                            return account_config['upload']['next_number']
                except Exception as e:
                    print(f"⚠️ 读取配置文件失败: {e}")
                
                # 如果配置读取失败，使用默认序号
                default_numbers = {
                    'ai_vanvan': 84,  # 当前进度
                    'aigf8728': 6,    # 从配置的起始序号开始
                    'gaoxiao': 1      # 新账号从1开始
                }
                return default_numbers.get(self.account_name, 1)
        except Exception as e:
            print(f"⚠️ 获取当前序号失败: {e}")
            return 1
    
    def _increment_episode_number(self) -> None:
        """仅在上传成功后增加序号"""
        try:
            # 按账号分开管理序号文件
            sequence_file = f"logs/episodes/{self.account_name}_episode.txt"
            
            if os.path.exists(sequence_file):
                with open(sequence_file, 'r', encoding='utf-8') as f:
                    current_number = int(f.read().strip())
            else:
                # 创建目录和文件
                os.makedirs(os.path.dirname(sequence_file), exist_ok=True)
                current_number = self._get_current_episode_number()
            
            # 增加序号
            with open(sequence_file, 'w', encoding='utf-8') as f:
                f.write(str(current_number + 1))
            print(f"📈 {self.account_name} 序号已更新: {current_number} → {current_number + 1}")
                
        except Exception as e:
            print(f"⚠️ 更新序号失败: {e}")
    
    def _get_next_episode_number(self) -> int:
        """获取下一个集数序号（已弃用，改用 _increment_episode_number）"""
        return self._get_current_episode_number()
    
    def _set_category_fast(self, category: str, subcategory: str = None):
        """优化的快速设置分区 - 避免误点击分区合集"""
        try:
            print(f"🏷️ 快速设置分区为: {category}")
            
            # 等待页面充分加载
            time.sleep(2)
            
            # 方法1：精确查找分区下拉选择器，排除"分区合集"
            category_set = False
            try:
                print("🔍 查找真正的分区选择器...")
                
                # 查找所有可能的选择器元素
                all_elements = self.driver.find_elements(By.XPATH, "//*[@class and (contains(@class, 'select') or contains(@class, 'dropdown') or contains(@class, 'category'))]")
                
                for element in all_elements:
                    if element.is_displayed() and element.is_enabled():
                        element_text = element.text.strip()
                        element_html = element.get_attribute('outerHTML')
                        
                        # 排除"分区合集"和其他不相关的元素
                        if any(exclude_word in element_text for exclude_word in ['分区合集', '合集', '添加', '上传', '发布']):
                            print(f"⚠️ 跳过非目标元素: {element_text}")
                            continue
                        
                        # 检查是否是真正的分区选择器
                        if (
                            ('分区' in element_text and len(element_text) < 10) or  # 简短的"分区"文字
                            'category' in element_html.lower() or
                            'type' in element_html.lower() or
                            ('select' in element_html.lower() and '分区' not in element_text)  # 没有文字但是select类
                        ):
                            print(f"🎯 找到候选分区选择器: '{element_text}' (tag: {element.tag_name})")
                            
                            try:
                                # 滚动并点击
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                time.sleep(0.5)
                                element.click()
                                time.sleep(1.5)
                                
                                # 尝试查找目标分区选项
                                try:
                                    category_option = WebDriverWait(self.driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, f"//*[text()='{category}']"))
                                    )
                                    category_option.click()
                                    print(f"✅ 已选择分区: {category}")
                                    category_set = True
                                    break
                                except:
                                    # 如果点击后没找到分区选项，说明点错了，继续尝试其他元素
                                    print(f"⚠️ 点击后未找到分区选项，继续尝试其他元素")
                                    continue
                                    
                            except Exception as e:
                                print(f"⚠️ 点击元素失败: {e}")
                                continue
                                
            except Exception as e1:
                print(f"方法1失败: {e1}")
            
            # 如果主方法没成功，使用更精确的备选方法
            if not category_set:
                print("🔄 使用精确备选方法...")
                category_set = self._set_category_precise_fallback(category, subcategory)
                if category_set:
                    return
            
            # 如果分区设置成功，继续设置子分区
            if category_set and subcategory:
                time.sleep(2)  # 等待子分区选项加载
                try:
                    subcategory_option = WebDriverWait(self.driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[text()='{subcategory}']"))
                    )
                    subcategory_option.click()
                    print(f"✅ 已选择子分区: {subcategory}")
                except Exception as e2:
                    print(f"⚠️ 子分区选择失败: {e2}")
                    # 尝试备选子分区查找
                    try:
                        subcategory_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{subcategory}')]")
                        for sub_elem in subcategory_elements:
                            if sub_elem.is_displayed():
                                sub_elem.click()
                                print(f"✅ 备选方法选择子分区: {subcategory}")
                                break
                    except:
                        print(f"⚠️ 备选子分区方法也失败")
                
        except Exception as e:
            print(f"⚠️ 分区设置出错: {e}")
            self._set_category_precise_fallback(category, subcategory)
    
    def _set_category_precise_fallback(self, category: str, subcategory: str = None) -> bool:
        """精确的分区设置备选方法 - 避免误点击分区合集"""
        try:
            print("🔄 执行精确备选分区设置方法...")
            
            # 方法1：通过标签查找，但排除"分区合集"
            try:
                # 查找所有可能的下拉菜单元素
                dropdown_elements = self.driver.find_elements(By.XPATH, "//select | //div[contains(@class, 'select')] | //div[contains(@class, 'dropdown')]")
                
                for element in dropdown_elements:
                    if element.is_displayed() and element.is_enabled():
                        element_text = element.text.strip()
                        
                        # 严格排除"分区合集"相关元素
                        if any(exclude in element_text for exclude in ['合集', '添加分P', '添加分p', '选择文件']):
                            continue
                            
                        try:
                            element.click()
                            time.sleep(1.5)
                            
                            # 查找分区选项
                            option = self.driver.find_element(By.XPATH, f"//*[text()='{category}']")
                            option.click()
                            print(f"✅ 精确备选方法设置分区: {category}")
                            
                            if subcategory:
                                time.sleep(1.5)
                                sub_option = self.driver.find_element(By.XPATH, f"//*[text()='{subcategory}']")
                                sub_option.click()
                                print(f"✅ 精确备选方法设置子分区: {subcategory}")
                            return True
                        except:
                            continue
            except:
                pass
            
            # 方法2：通过位置查找（分区选择器通常在页面上方）
            try:
                print("🔍 通过位置查找分区选择器...")
                
                # 查找页面上方的可点击元素
                clickable_elements = self.driver.find_elements(By.XPATH, "//*[@class and position() < 20]//div[contains(@class, 'select') or contains(@class, 'dropdown')]")
                
                for element in clickable_elements:
                    if element.is_displayed():
                        element_text = element.text.strip()
                        element_location = element.location
                        
                        # 确保元素在页面上方（y坐标较小）
                        if element_location['y'] < 800:  # 假设分区选择器在页面上方
                            # 排除明显不是分区选择器的元素
                            if any(exclude in element_text for exclude in ['合集', '文件', '上传', '发布']):
                                continue
                                
                            try:
                                element.click()
                                time.sleep(1.5)
                                
                                option = self.driver.find_element(By.XPATH, f"//*[text()='{category}']")
                                option.click()
                                print(f"✅ 位置方法设置分区: {category}")
                                
                                if subcategory:
                                    time.sleep(1.5)
                                    sub_option = self.driver.find_element(By.XPATH, f"//*[text()='{subcategory}']")
                                    sub_option.click()
                                    print(f"✅ 位置方法设置子分区: {subcategory}")
                                return True
                            except:
                                continue
            except:
                pass
                
            print("⚠️ 所有精确备选分区设置方法都失败")
            return False
            
        except Exception as e:
            print(f"⚠️ 精确备选分区设置出错: {e}")
            return False

    def _set_category_fallback(self, category: str, subcategory: str = None):
        """优化的分区设置备选方法"""
        try:
            print("🔄 执行备选分区设置方法...")
            
            # 备选方法1：查找包含"分区"文字的元素
            try:
                category_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '分区')]")
                for elem in category_elements:
                    if elem.is_displayed():
                        # 查找父级或相邻的可点击元素
                        try:
                            # 尝试点击包含分区的元素或其父级
                            clickable_elem = elem.find_element(By.XPATH, ".//*[@class] | .//following-sibling::*[1] | ..")
                            if clickable_elem.is_displayed():
                                clickable_elem.click()
                                time.sleep(1.5)
                                
                                # 查找分区选项
                                option = self.driver.find_element(By.XPATH, f"//*[text()='{category}']")
                                option.click()
                                print(f"✅ 备选方法1设置分区: {category}")
                                
                                if subcategory:
                                    time.sleep(1.5)
                                    sub_option = self.driver.find_element(By.XPATH, f"//*[text()='{subcategory}']")
                                    sub_option.click()
                                    print(f"✅ 备选方法1设置子分区: {subcategory}")
                                return
                        except:
                            continue
            except:
                pass
            
            # 备选方法2：通过标签和类名查找
            try:
                selectors = [
                    "//select",
                    "//div[contains(@class, 'select')]",
                    "//div[contains(@class, 'dropdown')]",
                    "//div[contains(@class, 'category')]",
                    "//button[contains(@class, 'select')]"
                ]
                
                for selector in selectors:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            try:
                                element.click()
                                time.sleep(1)
                                
                                # 查找目标分区
                                option = self.driver.find_element(By.XPATH, f"//*[text()='{category}']")
                                option.click()
                                print(f"✅ 备选方法2设置分区: {category}")
                                
                                if subcategory:
                                    time.sleep(1)
                                    sub_option = self.driver.find_element(By.XPATH, f"//*[text()='{subcategory}']")
                                    sub_option.click()
                                    print(f"✅ 备选方法2设置子分区: {subcategory}")
                                return
                            except:
                                continue
            except:
                pass
                
            print("⚠️ 所有备选分区设置方法都失败")
            
        except Exception as e:
            print(f"⚠️ 备选分区设置出错: {e}")
    
    def _submit_and_wait_success(self) -> bool:
        """提交投稿并等待成功"""
        try:
            print("📋 准备提交投稿...")
            
            # 滚动到页面底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # 快速定位立即投稿按钮
            try:
                submit_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='立即投稿']"))
                )
                
                print("🎯 找到立即投稿按钮")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                time.sleep(0.5)
                
                # 点击投稿
                ActionChains(self.driver).move_to_element(submit_button).pause(0.5).click().perform()
                print("✅ 立即投稿按钮已点击")
                
            except Exception:
                # 备选方法
                spans = self.driver.find_elements(By.TAG_NAME, "span")
                for span in spans:
                    if span.is_displayed() and span.text.strip() == "立即投稿":
                        ActionChains(self.driver).move_to_element(span).click().perform()
                        print("✅ 立即投稿按钮已点击 (备选方法)")
                        break
                else:
                    print("❌ 未找到立即投稿按钮")
                    return False
            
            # 处理确认弹窗
            try:
                confirm = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '确定') or contains(text(), '确认')]"))
                )
                confirm.click()
                print("✅ 已点击确认按钮")
            except:
                pass
            
            # 等待"稿件投递成功"提示
            print("🔍 等待稿件投递成功提示...")
            try:
                success_element = WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'稿件投递成功')]"))
                )
                print("🎉 检测到'稿件投递成功'提示！")
                
                # 截图保存
                try:
                    import datetime
                    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_dir = "c:/Code/social-media-hub/temp"
                    os.makedirs(screenshot_dir, exist_ok=True)
                    screenshot_path = f"{screenshot_dir}/稿件投递成功_{now}.png"
                    self.driver.save_screenshot(screenshot_path)
                    print(f"📸 已保存成功截图: {screenshot_path}")
                except Exception as e:
                    print(f"⚠️ 截图保存失败: {e}")
                    
                print("✅ 稿件投递成功！")
                
                # 上传成功后才增加序号
                self._increment_episode_number()
                
                # 上传成功后关闭浏览器（所有账户）
                print("🎉 上传成功！3秒后关闭浏览器...")
                time.sleep(3)
                if hasattr(self, 'driver') and self.driver:
                    self.driver.quit()
                    print("✅ 浏览器已关闭")
                return True
                
            except Exception:
                print("⚠️ 等待120秒后未检测到'稿件投递成功'")
                print(f"🔄 保持当前序号: {getattr(self, 'current_episode_number', '未知')}")
                
                # 上传超时，关闭浏览器
                print("⏰ 上传超时，关闭浏览器...")
                if hasattr(self, 'driver') and self.driver:
                    self.driver.quit()
                return False
                
        except Exception as e:
            print(f"❌ 提交过程失败: {e}")
            print(f"🔄 保持当前序号: {getattr(self, 'current_episode_number', '未知')}")
            
            # 提交失败，关闭浏览器
            print("关闭浏览器...")
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
            return False
