import sys
sys.path.insert(0, 'src')
from utils.logger import Logger

logger = Logger('ai_vanvan')
unmerged = logger.get_unmerged_downloads()

print(f'未合并视频总数: {len(unmerged)}')
print(f'\n前3个未合并视频:')
for i, v in enumerate(unmerged[:3]):
    print(f'{i+1}. shortcode: {v["shortcode"]}')
    print(f'   文件夹: {v.get("download_folder", v.get("file_path"))}')
    print(f'   博主: {v.get("blogger_name", "unknown")}')
    print()
