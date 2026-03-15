#!/usr/bin/env python3
"""测试check_if_downloaded函数"""
import os
import lzma
import json

def check_if_downloaded(account_name, shortcode):
    """检查视频是否已经下载（通过检查.json.xz文件）"""
    download_dir = f"/app/downloads/{account_name}"
    if not os.path.exists(download_dir):
        print(f"⚠️ 下载目录不存在: {download_dir}")
        return False
    
    def check_json_files_in_dir(directory):
        """检查目录中的JSON.xz文件"""
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.json.xz'):
                    json_file_path = os.path.join(directory, filename)
                    try:
                        with open(json_file_path, 'rb') as f:
                            content = lzma.decompress(f.read()).decode('utf-8')
                            data = json.loads(content)
                            
                            # instaloader的数据结构：shortcode在node层级
                            node = data.get('node', {})
                            file_shortcode = node.get('shortcode')
                            if file_shortcode == shortcode:
                                print(f"✅ 找到已下载: {shortcode} in {directory}/{filename}")
                                return True
                    except Exception as e:
                        continue
            return False
        except Exception as e:
            print(f"❌ 检查目录失败 {directory}: {e}")
            return False
    
    # 1. 首先检查账户根目录下的JSON文件
    print(f"\n🔍 检查根目录: {download_dir}")
    if check_json_files_in_dir(download_dir):
        return True
    
    # 2. 然后检查日期子目录下的JSON文件
    print(f"🔍 检查子目录...")
    try:
        for date_folder in os.listdir(download_dir):
            date_folder_path = os.path.join(download_dir, date_folder)
            if os.path.isdir(date_folder_path):
                print(f"   📁 检查 {date_folder}/")
                if check_json_files_in_dir(date_folder_path):
                    return True
    except Exception as e:
        print(f"❌ 检查子目录失败: {e}")
                    
    return False

# 测试今天下载的几个shortcode
test_shortcodes = [
    'DKS1nTJyWhY',
    'DMLRQLZtjan', 
    'DPV2h77iAlK',
    'DOcURh6ktUy',
    'DXXXNotExist'  # 这个不存在
]

print("=" * 60)
print("测试 check_if_downloaded 函数")
print("=" * 60)

for shortcode in test_shortcodes:
    print(f"\n{'='*60}")
    print(f"测试: {shortcode}")
    print('='*60)
    result = check_if_downloaded('ai_vanvan', shortcode)
    print(f"\n结果: {'✅ 已下载' if result else '❌ 未下载'}")
