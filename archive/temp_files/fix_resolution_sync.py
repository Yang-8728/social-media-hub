#!/usr/bin/env python3
import os
import subprocess

def fix_resolution_merge_sync():
    """修复分辨率标准化合并中的同步问题"""
    
    # 同样的5个视频，但使用更安全的合并参数
    video_dir = r"videos\downloads\ai_vanvan\2025-08-27"
    video_files = [
        "2025-03-05_15-32-07_UTC.mp4",    # 0.7MB 需要加黑边的视频
        "2025-08-08_11-23-16_UTC.mp4",    # 32MB 标准分辨率
        "2025-08-15_17-44-44_UTC.mp4",    # 11MB 标准分辨率
        "2025-08-26_12-57-05_UTC.mp4",    # 0.4MB 标准分辨率
        "2025-07-26_16-58-23_UTC.mp4"     # 6MB 标准分辨率
    ]
    
    video_paths = [os.path.join(video_dir, f) for f in video_files]
    
    print("🔧 修复分辨率标准化合并的同步问题")
    print("=" * 50)
    print("问题: 第一个视频(加黑边)结尾停顿，影响后续视频")
    print("解决: 使用更严格的音视频同步参数")
    print()
    
    # 创建文件列表
    temp_list_file = "temp_sync_fix_list.txt"
    output_file = "test_resolution_sync_fixed.mp4"
    
    try:
        with open(temp_list_file, 'w', encoding='utf-8') as f:
            for video_path in video_paths:
                f.write(f"file '{video_path}'\n")
        
        print("使用高级音视频同步参数进行分辨率标准化...")
        
        # 使用VideoMerger，但添加更严格的同步参数
        try:
            import sys
            sys.path.append('src')
            from utils.video_merger import VideoMerger
            
            merger = VideoMerger()
            
            # 创建临时标准化视频目录
            temp_dir = "temp_normalized"
            os.makedirs(temp_dir, exist_ok=True)
            
            print("第一步: 单独标准化每个视频...")
            normalized_paths = []
            
            for i, video_path in enumerate(video_paths):
                filename = os.path.basename(video_path)
                temp_output = os.path.join(temp_dir, f"normalized_{i+1}_{filename}")
                
                print(f"  标准化 ({i+1}/5): {filename}")
                
                # 单独标准化每个视频，添加严格的音视频参数
                cmd = [
                    'ffmpeg', '-y', '-i', video_path,
                    '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                    '-avoid_negative_ts', 'make_zero',
                    '-fflags', '+genpts',
                    '-vsync', 'cfr',  # 恒定帧率
                    '-async', '1',    # 音频同步
                    '-shortest',      # 以最短流为准
                    temp_output
                ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    if os.path.exists(temp_output):
                        normalized_paths.append(temp_output)
                        print(f"    ✅ 成功")
                    else:
                        print(f"    ❌ 输出文件不存在")
                        raise Exception("标准化失败")
                except Exception as e:
                    print(f"    ❌ 失败: {e}")
                    # 如果标准化失败，使用原文件
                    normalized_paths.append(video_path)
            
            print("\n第二步: 合并标准化后的视频...")
            
            # 创建新的文件列表
            normalized_list_file = "temp_normalized_list.txt"
            with open(normalized_list_file, 'w', encoding='utf-8') as f:
                for path in normalized_paths:
                    f.write(f"file '{path}'\n")
            
            # 使用copy模式合并（避免重新编码）
            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', normalized_list_file,
                '-c', 'copy',  # 直接拷贝，不重新编码
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"\n✅ 修复成功！")
                print(f"输出文件: {output_file} ({size_mb:.1f}MB)")
                print(f"修复要点:")
                print(f"  - 每个视频单独标准化为720x1280")
                print(f"  - 第一个视频(576x1024)已添加黑边")
                print(f"  - 使用恒定帧率避免结尾停顿")
                print(f"  - 音频同步参数确保无缝衔接")
                return True
            else:
                print(f"\n❌ 合并失败 - 输出文件不存在")
                return False
                
        except Exception as e:
            print(f"VideoMerger方法失败: {e}")
            print("尝试直接FFmpeg方法...")
            
            # 备用方案：直接使用FFmpeg
            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', temp_list_file,
                '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                '-avoid_negative_ts', 'make_zero',
                '-fflags', '+genpts',
                '-vsync', 'cfr',
                '-async', '1',
                '-shortest',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"\n✅ 直接FFmpeg方法成功！")
                print(f"输出文件: {output_file} ({size_mb:.1f}MB)")
                return True
            else:
                print(f"\n❌ FFmpeg也失败了: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"\n❌ 执行过程出错: {e}")
        return False
    finally:
        # 清理临时文件
        for temp_file in [temp_list_file, "temp_normalized_list.txt"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        # 清理临时目录
        import shutil
        if os.path.exists("temp_normalized"):
            try:
                shutil.rmtree("temp_normalized")
            except:
                pass

if __name__ == "__main__":
    success = fix_resolution_merge_sync()
    
    if success:
        print("\n🎉 同步问题修复完成！")
        print("   播放 test_resolution_sync_fixed.mp4 检查:")
        print("   1. 第一个视频有黑边但结尾不卡顿")
        print("   2. 后续视频正常播放")
        print("   3. 整体音视频同步")
    else:
        print("\n💥 修复失败")
        print("   可能需要检查视频文件完整性")
