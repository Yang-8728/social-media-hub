"""
检查json.xz文件格式
"""
import lzma
import json
from pathlib import Path

def check_json_files():
    folder_path = Path("videos/downloads/ai_vanvan/2025-08-27")
    json_files = list(folder_path.glob("*.json.xz"))
    
    print(f"找到 {len(json_files)} 个json.xz文件")
    
    for i, json_file in enumerate(json_files[:3]):  # 只检查前3个
        print(f"\n🔍 检查文件: {json_file.name}")
        try:
            with open(json_file, 'rb') as f:
                # 先检查文件大小
                file_size = json_file.stat().st_size
                print(f"  文件大小: {file_size} 字节")
                
                # 尝试解压
                compressed_data = f.read()
                print(f"  压缩数据长度: {len(compressed_data)}")
                
                try:
                    content = lzma.decompress(compressed_data).decode('utf-8')
                    print(f"  解压后长度: {len(content)}")
                    
                    # 显示前200个字符
                    print(f"  内容预览: {content[:200]}...")
                    
                    # 尝试解析JSON
                    metadata = json.loads(content)
                    shortcode = metadata.get('shortcode')
                    owner = metadata.get('owner', {}).get('username', 'unknown')
                    print(f"  ✅ shortcode: {shortcode}")
                    print(f"  ✅ owner: {owner}")
                    
                except lzma.LZMAError as e:
                    print(f"  ❌ LZMA解压失败: {e}")
                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON解析失败: {e}")
                    
        except Exception as e:
            print(f"  ❌ 文件读取失败: {e}")

if __name__ == "__main__":
    check_json_files()
