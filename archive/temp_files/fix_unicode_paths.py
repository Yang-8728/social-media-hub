import os
import shutil

def move_unicode_files_to_standard():
    """将Unicode路径中的文件移动到标准路径"""
    base_path = r'c:\Code\social-media-hub'
    print(f"搜索基础路径: {base_path}")
    
    total_found = 0
    total_moved = 0
    
    # 查找所有Unicode路径中的文件
    for root, dirs, files in os.walk(base_path):
        if '﹨' in root and files:  # 如果路径包含Unicode分隔符且有文件
            total_found += len(files)
            print(f"\n发现Unicode路径: {root}")
            print(f"  包含 {len(files)} 个文件")
            
            # 计算对应的标准路径
            standard_root = root.replace('﹨', '\\')
            print(f"  对应标准路径: {standard_root}")
            
            # 确保标准路径目录存在
            os.makedirs(standard_root, exist_ok=True)
            
            # 移动每个文件
            moved_count = 0
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(standard_root, file)
                
                try:
                    if not os.path.exists(dst_path):  # 避免覆盖
                        shutil.move(src_path, dst_path)
                        print(f"    ✅ 移动: {file}")
                        moved_count += 1
                    else:
                        print(f"    ⚠️  跳过 (已存在): {file}")
                except Exception as e:
                    print(f"    ❌ 移动失败 {file}: {e}")
            
            total_moved += moved_count
            print(f"  成功移动 {moved_count} 个文件")
            
            # 如果Unicode目录现在是空的，删除它
            try:
                if not os.listdir(root):
                    os.rmdir(root)
                    print(f"  🗑️  删除空目录: {root}")
            except:
                pass
    
    print(f"\n=== 汇总 ===")
    print(f"发现文件总数: {total_found}")
    print(f"成功移动文件: {total_moved}")

if __name__ == "__main__":
    print("=== 移动Unicode路径文件到标准路径 ===")
    move_unicode_files_to_standard()
    print("=== 完成 ===")
