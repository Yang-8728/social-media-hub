"""
正确解析instaloader的json.xz格式
"""
import lzma
import json
from pathlib import Path

def parse_instaloader_json():
    folder_path = Path("videos/downloads/ai_vanvan/2025-08-27")
    json_files = list(folder_path.glob("*.json.xz"))
    
    print(f"找到 {len(json_files)} 个json.xz文件")
    
    for json_file in json_files[:3]:  # 检查前3个
        print(f"\n🔍 文件: {json_file.name}")
        try:
            with open(json_file, 'rb') as f:
                content = lzma.decompress(f.read()).decode('utf-8')
                data = json.loads(content)
                
                # instaloader的数据结构
                node = data.get('node', {})
                
                # 从不同可能的位置提取shortcode
                shortcode = node.get('shortcode')
                
                # 如果没有shortcode，尝试从URL中提取
                if not shortcode:
                    # 有时候shortcode在其他字段
                    print(f"  可用字段: {list(node.keys())[:10]}")
                    
                    # 尝试从文件名提取（最后的备选方案）
                    # instaloader的文件名格式通常是: YYYY-MM-DD_HH-MM-SS_UTC
                    filename_base = json_file.stem.replace('.json', '')
                    print(f"  文件名基础: {filename_base}")
                
                # 提取owner信息
                owner_info = node.get('owner', {})
                owner_username = owner_info.get('username', 'unknown')
                
                print(f"  shortcode: {shortcode}")
                print(f"  owner: {owner_username}")
                print(f"  id: {node.get('id')}")
                
                # 查看数据结构中是否有其他识别信息
                display_url = node.get('display_url', '')
                if display_url:
                    print(f"  display_url: {display_url[:100]}...")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")

if __name__ == "__main__":
    parse_instaloader_json()
