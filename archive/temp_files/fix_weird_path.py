import os
import shutil

print("=== 处理异常Unicode目录中的文件 ===")

# 异常目录路径
weird_path = r'c：\Code\social-media-hub\videos\downloads\ai_vanvan\2025-08-27'
correct_path = r'videos\downloads\ai_vanvan\2025-08-27'

print(f"异常路径: {weird_path}")
print(f"正确路径: {correct_path}")

# 确保正确路径存在
os.makedirs(correct_path, exist_ok=True)

# 检查异常目录中的文件
if os.path.exists(weird_path):
    files = os.listdir(weird_path)
    print(f"\n发现 {len(files)} 个文件:")
    
    moved_count = 0
    for file in files:
        src = os.path.join(weird_path, file)
        dst = os.path.join(correct_path, file)
        
        print(f"  {file}")
        
        # 检查目标文件是否已存在
        if os.path.exists(dst):
            # 比较文件大小
            src_size = os.path.getsize(src)
            dst_size = os.path.getsize(dst)
            
            if src_size == dst_size:
                print(f"    ✅ 文件已存在且大小相同，删除重复文件")
                os.remove(src)
            else:
                print(f"    ⚠️  文件已存在但大小不同 (源:{src_size}, 目标:{dst_size})")
                backup_name = f"{file}.backup"
                backup_path = os.path.join(correct_path, backup_name)
                shutil.move(src, backup_path)
                print(f"    📦 移动为备份: {backup_name}")
                moved_count += 1
        else:
            # 移动文件
            shutil.move(src, dst)
            print(f"    ✅ 移动到正确位置")
            moved_count += 1
    
    print(f"\n处理完成: 移动/备份了 {moved_count} 个文件")
    
    # 删除空的异常目录结构
    try:
        # 从最深层开始删除空目录
        current_path = weird_path
        while current_path and current_path != 'c：':
            if os.path.exists(current_path) and not os.listdir(current_path):
                os.rmdir(current_path)
                print(f"✅ 删除空目录: {current_path}")
                current_path = os.path.dirname(current_path)
            else:
                break
                
        # 最后删除根异常目录
        if os.path.exists('c：'):
            try:
                shutil.rmtree('c：')
                print(f"✅ 删除整个异常目录树: c：")
            except Exception as e:
                print(f"⚠️  无法删除根异常目录: {e}")
                
    except Exception as e:
        print(f"⚠️  清理目录时出错: {e}")
        
else:
    print("异常目录不存在")

print(f"\n🎯 验证正确路径中的文件:")
if os.path.exists(correct_path):
    correct_files = os.listdir(correct_path)
    print(f"正确位置现在有 {len(correct_files)} 个文件:")
    for file in sorted(correct_files):
        size_mb = os.path.getsize(os.path.join(correct_path, file)) / (1024*1024)
        print(f"  - {file} ({size_mb:.1f}MB)")
else:
    print("正确路径不存在")
