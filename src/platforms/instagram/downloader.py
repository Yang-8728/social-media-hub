"""
Instagram 下载器实现
基于 instaloader 实现 Instagram 内容下载
"""
import os
import sys
import contextlib
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect
from instaloader import Instaloader, ConnectionException
from typing import List, Any

from ...core.interfaces import IDownloader
from ...core.models import Account, Post, DownloadResult
from ...utils.logger import Logger
from ...utils.path_utils import clean_unicode_path
from ...utils.account_mapping import get_display_name


class InstagramDownloader(IDownloader):
    """Instagram 下载器"""
    
    def __init__(self):
        self.loader = None
        self.logger = None

    @contextlib.contextmanager
    def suppress_instaloader_errors(self):
        """抑制instaloader的错误输出"""
        import io
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()
        try:
            yield
        finally:
            sys.stderr = old_stderr

    def get_cookiefile(self):
        """获取 Firefox cookies 文件路径"""
        if system() == "Windows":
            # Windows Firefox cookies 路径
            firefox_dir = os.path.join(expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
            for profile in glob(os.path.join(firefox_dir, "*")):
                if os.path.isdir(profile):
                    cookiefile = os.path.join(profile, "cookies.sqlite")
                    if os.path.exists(cookiefile):
                        return cookiefile
        else:
            # Linux/Mac Firefox cookies 路径
            firefox_dir = os.path.join(expanduser("~"), ".mozilla", "firefox")
            for profile in glob(os.path.join(firefox_dir, "*")):
                if os.path.isdir(profile):
                    cookiefile = os.path.join(profile, "cookies.sqlite")
                    if os.path.exists(cookiefile):
                        return cookiefile
        return None

    def get_session_file_path(self, username: str) -> str:
        """获取 session 文件路径"""
        session_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(session_dir, exist_ok=True)
        return os.path.join(session_dir, f"{username}_session")

    def validate_login(self, cookiefile, input_username):
        """验证登录状态"""
        conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
        try:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
            )
        except OperationalError:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
            )

        loader = Instaloader(max_connection_attempts=1)
        loader.context._session.cookies.update(cookie_data)

        actual_username = loader.test_login()
        return actual_username == input_username

    def login(self, account: Account) -> bool:
        """登录 Instagram 账号"""
        # Logger 直接使用账号名称
        self.logger = Logger(account.name)
        
        try:
            # 创建安全的 Instaloader 实例，限制请求频率和禁用输出
            self.loader = Instaloader(
                max_connection_attempts=3,  # 最大连接尝试次数
                request_timeout=10,        # 请求超时时间
                quiet=True,                # 禁用输出
                save_metadata=False        # 不保存元数据文件
            )
            
            # 尝试从 session 文件登录
            session_file = self.get_session_file_path(account.username)
            if os.path.exists(session_file):
                print(f"Loaded session from {session_file}.")
                self.loader.load_session_from_file(account.username, session_file)
                self.loader.context.username = account.username  # 关键设置！
                
                # 静默测试登录，抑制错误输出
                try:
                    with self.suppress_instaloader_errors():
                        if self.loader.test_login() == account.username:
                            self.logger.success(f"从 session 文件登录成功: {account.username}")
                            return True
                except Exception:
                    pass  # 忽略session检查错误，继续使用Firefox cookies
            
            # 尝试从 Firefox cookies 登录
            cookiefile = self.get_cookiefile()
            if self.validate_login(cookiefile, account.username):
                conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
                try:
                    cookie_data = conn.execute(
                        "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
                    )
                except OperationalError:
                    cookie_data = conn.execute(
                        "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
                    )
                
                self.loader.context._session.cookies.update(cookie_data)
                self.loader.context.username = account.username  # 设置用户名
                self.loader.save_session_to_file(session_file)
                self.logger.success(f"从 Firefox cookies 登录成功: {account.username}")
                return True
            
            self.logger.error(f"登录失败: {account.username}")
            return False
            
        except Exception as e:
            self.logger.error(f"登录过程出错: {e}")
            return False

    def get_post_owner(self, post) -> str:
        """获取帖子所有者"""
        try:
            if hasattr(post, 'owner_username'):
                return post.owner_username
            elif hasattr(post, 'owner') and hasattr(post.owner, 'username'):
                return post.owner.username
            else:
                return "unknown"
        except Exception as e:
            self.logger.warning(f"无法获取帖子所有者: {e}")
            return "unknown"

    def download_posts(self, account: Account, count: int = 10) -> List[DownloadResult]:
        """下载帖子"""
        import time
        from ...utils.folder_manager import FolderManager
        
        if not self.loader or not self.logger:
            if not self.login(account):
                return [DownloadResult(success=False, posts=[], message="登录失败")]
        
        try:
            # 获取配置
            from main import load_account_config
            config = load_account_config()
            account_config = config.get(account.name, {})
            
            # 安全设置
            safety_config = account_config.get("download_safety", {})
            max_posts = safety_config.get("max_posts_per_session", 50)
            request_delay = safety_config.get("request_delay", 2)
            
            # 限制处理数量
            MAX_PROCESS_COUNT = min(count, max_posts)
            
            # 直接使用账号名显示
            self.logger.info(f"开始下载任务：{account.name}")
            
            # 初始化文件夹管理器
            folder_manager = FolderManager(account.name, account_config)
            
            # 获取保存的帖子
            from instaloader import Profile
            profile = Profile.from_username(self.loader.context, account.username)
            saved_posts = profile.get_saved_posts()
            
            # 预扫描：统计新视频数量
            self.logger.info("正在扫描新视频...")
            new_videos = []
            scan_count = 0
            scan_limit = min(MAX_PROCESS_COUNT, 50)  # 最多扫描50个posts，避免被封
            
            for post in saved_posts:
                scan_count += 1
                if scan_count > scan_limit:
                    # 静默停止扫描，不显示日志
                    break
                    
                shortcode = post.shortcode
                if not self.logger.is_downloaded(shortcode):
                    new_videos.append(post)
                    if len(new_videos) >= MAX_PROCESS_COUNT:
                        break  # 找到足够的新视频就停止扫描
            
            actual_download_count = min(len(new_videos), MAX_PROCESS_COUNT)
            self.logger.info(f"发现 {len(new_videos)} 个新视频，准备下载 {actual_download_count} 个")
            
            if len(new_videos) == 0:
                self.logger.info("没有新视频需要下载")
                return [DownloadResult(success=True, posts=[], message="没有新视频")]
            
            downloaded_count = 0
            skipped_count = 0
            failed_count = 0
            posts = []
            
            # 用于批量显示跳过信息
            last_skip_report = 0
            skip_report_interval = 10  # 每10个跳过显示一次
            
            # 记录开始时间
            import time
            start_time = time.time()
            
            for i, post in enumerate(new_videos):
                # 如果已经下载了足够数量的新视频，就停止
                if downloaded_count >= actual_download_count:
                    self.logger.warning(f"达到计划下载数量限制 ({actual_download_count})，停止下载")
                    break
                
                try:
                    shortcode = post.shortcode
                    # 由于是预扫描的新视频，理论上不应该跳过，但为了安全还是检查一下
                    if self.logger.is_downloaded(shortcode):
                        skipped_count += 1
                        # 批量显示跳过信息，避免日志过多
                        if skipped_count - last_skip_report >= skip_report_interval:
                            self.logger.info(f"已跳过 {skipped_count} 个已下载的视频...")
                            last_skip_report = skipped_count
                        continue  # 跳过已下载的，不计入下载数量限制
                    
                    # 获取帖子所有者
                    post_owner = self.get_post_owner(post)
                    
                    # 获取下载文件夹
                    download_folder = folder_manager.get_download_folder(post_owner)
                    # 使用专用函数确保路径正确
                    download_folder = clean_unicode_path(download_folder)
                    os.makedirs(download_folder, exist_ok=True)
                    
                    # 静默下载帖子，抑制错误输出
                    with self.suppress_instaloader_errors():
                        self.loader.download_post(post, target=download_folder)
                    
                    # 记录下载成功
                    post_obj = Post(
                        shortcode=shortcode,
                        url=f"https://www.instagram.com/p/{shortcode}/",
                        caption=post.caption or "",
                        date=post.date_utc
                    )
                    posts.append(post_obj)
                    
                    # 静默记录下载成功，不显示日志
                    self.logger.record_download(shortcode, "success", download_folder, folder=download_folder, blogger=post_owner)
                    downloaded_count += 1
                    
                    # 计算进度和用时
                    progress = (downloaded_count / actual_download_count) * 100
                    elapsed_time = time.time() - start_time
                    
                    # 格式化时间显示
                    if elapsed_time >= 60:
                        minutes = int(elapsed_time // 60)
                        seconds = int(elapsed_time % 60)
                        time_str = f"{minutes}分{seconds}秒"
                    else:
                        time_str = f"{int(elapsed_time)}秒"
                    
                    # 进度条显示（更新在同一行）
                    progress_bar = "█" * int(progress // 5) + "░" * (20 - int(progress // 5))
                    
                    # 使用 \r 回到行首，覆盖之前的进度条
                    print(f"\r下载进度: ({downloaded_count}/{actual_download_count}) [{progress:.1f}%] [{progress_bar}] 用时: {time_str}", end="", flush=True)
                    
                    # 如果是最后一个，换行
                    if downloaded_count == actual_download_count:
                        print()  # 换行
                        self.logger.success(f"下载完成")
                    
                    # 安全延迟
                    time.sleep(request_delay)
                    
                except Exception as e:
                    self.logger.error(f"下载失败: {e}")
                    failed_count += 1
            
            # 计算总用时
            total_time = time.time() - start_time
            if total_time >= 60:
                minutes = int(total_time // 60)
                seconds = int(total_time % 60)
                total_time_str = f"{minutes}分{seconds}秒"
            else:
                total_time_str = f"{int(total_time)}秒"
            
            # 获取存储文件夹路径
            download_folder = folder_manager.get_download_folder()
            
            # 最终汇总信息
            print()  # 换行，确保汇总信息在新行显示
            self.logger.info("=" * 50)
            self.logger.info(f"下载任务完成！")
            self.logger.info(f"成功下载: {downloaded_count} 个视频")
            self.logger.info(f"跳过已有: {skipped_count} 个视频") 
            self.logger.info(f"下载失败: {failed_count} 个视频")
            self.logger.info(f"总用时: {total_time_str}")
            self.logger.info(f"保存位置: {download_folder}")
            self.logger.info("=" * 50)
            
            return [DownloadResult(
                success=True,
                posts=posts,
                message=f"成功下载 {downloaded_count} 个帖子，跳过 {skipped_count} 个，失败 {failed_count} 个，用时 {total_time_str}"
            )]
            
        except Exception as e:
            self.logger.error(f"下载过程出错: {e}")
            return [DownloadResult(success=False, posts=[], message=str(e))]

    def setup_session(self, account_name: str) -> bool:
        """设置下载会话"""
        # 从配置文件加载账号信息
        from main import load_account_config, create_account_from_config
        config = load_account_config()
        account = create_account_from_config(account_name, config)
        return self.login(account)
    
    def download_saved_posts(self, account_name: str, limit: int = None) -> List[Any]:
        """下载保存的帖子"""
        # 从配置文件加载账号信息
        from main import load_account_config, create_account_from_config
        config = load_account_config()
        account = create_account_from_config(account_name, config)
        
        # 设置默认限制
        if limit is None:
            limit = 10
            
        return self.download_posts(account, limit)
