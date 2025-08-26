"""
Bilibili 上传器接口
"""
from typing import List
from ...core.interfaces import IUploader
from ...core.models import Account, Video, UploadResult

class BilibiliUploader(IUploader):
    """Bilibili 上传器"""
    
    def __init__(self):
        self.driver = None
    
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
