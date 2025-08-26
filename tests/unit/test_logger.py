#!/usr/bin/env python3
"""
日志模块单元测试
"""
import sys
import os
import tempfile
import shutil
import unittest

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.utils.logger import Logger

class TestLogger(unittest.TestCase):
    """日志模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_account = "test_logger"
        self.logger = Logger(self.test_account)
    
    def test_record_download_success(self):
        """测试记录成功下载"""
        shortcode = "test_shortcode_001"
        file_path = "/path/to/video.mp4"
        
        self.logger.record_download(shortcode, "success", file_path)
        
        # 检查记录是否正确保存
        log_data = self.logger.load_download_log()
        downloads = log_data["downloads"]
        
        self.assertEqual(len(downloads), 1)
        self.assertEqual(downloads[0]["shortcode"], shortcode)
        self.assertEqual(downloads[0]["status"], "success")
        self.assertEqual(downloads[0]["file_path"], file_path)
    
    def test_get_unmerged_downloads(self):
        """测试获取未合并下载"""
        # 记录几个下载
        self.logger.record_download("code1", "success", "/path/video1.mp4")
        self.logger.record_download("code2", "success", "/path/video2.mp4")
        self.logger.record_download("code3", "failed", error="网络错误")
        
        unmerged = self.logger.get_unmerged_downloads()
        
        # 应该有2个成功且未合并的
        self.assertEqual(len(unmerged), 2)
        self.assertEqual(unmerged[0]["shortcode"], "code1")
        self.assertEqual(unmerged[1]["shortcode"], "code2")
    
    def test_mark_as_merged(self):
        """测试标记为已合并"""
        # 先记录一些下载
        self.logger.record_download("merge1", "success", "/path/video1.mp4")
        self.logger.record_download("merge2", "success", "/path/video2.mp4")
        
        # 标记为已合并
        self.logger.mark_as_merged(["merge1", "merge2"], "/path/merged.mp4")
        
        # 检查未合并列表
        unmerged = self.logger.get_unmerged_downloads()
        self.assertEqual(len(unmerged), 0)
        
        # 检查合并会话记录
        log_data = self.logger.load_download_log()
        merged_sessions = log_data["merged_sessions"]
        self.assertEqual(len(merged_sessions), 1)
        self.assertEqual(merged_sessions[0]["video_count"], 2)

def run_logger_tests():
    """运行日志模块测试"""
    print("=== 日志模块单元测试 ===")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogger)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_logger_tests()
    sys.exit(0 if success else 1)
