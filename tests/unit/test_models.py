#!/usr/bin/env python3
"""
数据模型单元测试
"""
import sys
import os
import unittest
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.core.models import Account, Post, Video, DownloadResult, UploadResult

class TestModels(unittest.TestCase):
    """数据模型测试类"""
    
    def test_account_creation(self):
        """测试账号创建"""
        account = Account(
            name="test_account",
            platform="instagram",
            username="test_user"
        )
        
        self.assertEqual(account.name, "test_account")
        self.assertEqual(account.platform, "instagram")
        self.assertEqual(account.username, "test_user")
    
    def test_post_creation(self):
        """测试帖子创建"""
        post = Post(
            shortcode="ABC123",
            url="https://instagram.com/p/ABC123/",
            caption="测试帖子",
            date=datetime.now()
        )
        
        self.assertEqual(post.shortcode, "ABC123")
        self.assertEqual(post.url, "https://instagram.com/p/ABC123/")
        self.assertEqual(post.caption, "测试帖子")
        self.assertEqual(len(post.media_urls), 0)  # 默认为空列表
    
    def test_download_result(self):
        """测试下载结果"""
        posts = [
            Post("code1", "url1"),
            Post("code2", "url2")
        ]
        
        result = DownloadResult(
            success=True,
            posts=posts,
            message="下载成功"
        )
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.posts), 2)
        self.assertEqual(result.message, "下载成功")
        self.assertEqual(result.error, "")  # 默认为空
    
    def test_upload_result(self):
        """测试上传结果"""
        result = UploadResult(
            success=False,
            error="上传失败"
        )
        
        self.assertFalse(result.success)
        self.assertEqual(result.error, "上传失败")
        self.assertEqual(result.video_id, "")  # 默认为空

def run_models_tests():
    """运行数据模型测试"""
    print("=== 数据模型单元测试 ===")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_models_tests()
    sys.exit(0 if success else 1)
