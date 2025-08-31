#!/usr/bin/env python3
"""
Re-merge a specific merged video by reading its source clip list from the download log.
Outputs a new file with _fixed suffix using the normalization + concat filter pipeline.
"""
import json
import os
import sys
from glob import glob

# Allow imports from src
sys.path.append('src')
from utils.video_merger import VideoMerger

ACCOUNT = 'ai_vanvan'
TARGET_BASENAME = '2025-08-30_2.mp4'  # the original merged filename to re-merge

LOG_PATH = os.path.join('videos', 'download_logs', f'{ACCOUNT}_downloads.json')
DOWNLOADS_ROOT = os.path.join('videos', 'downloads', ACCOUNT)
MERGED_ROOT = os.path.join('videos', 'merged', ACCOUNT)


def find_session(log_data, target_basename: str):
    sessions = log_data.get('merged_sessions', [])
    for s in sessions:
        path = s.get('merged_file_path') or ''
        if os.path.basename(path) == target_basename:
            return s
    return None


def find_clip(full_basename: str) -> str | None:
    # search recursively under downloads root
    pattern = os.path.join(DOWNLOADS_ROOT, '**', full_basename)
    matches = glob(pattern, recursive=True)
    return matches[0] if matches else None


def main():
    if not os.path.exists(LOG_PATH):
        print(f'Log not found: {LOG_PATH}')
        sys.exit(1)

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        log_data = json.load(f)

    session = find_session(log_data, TARGET_BASENAME)
    if not session:
        print(f'No merged session found for: {TARGET_BASENAME}')
        sys.exit(2)

    merged_files = session.get('merged_files') or []
    if not merged_files:
        print('Session has no merged_files list')
        sys.exit(3)

    # Resolve full paths in the same order
    clip_paths = []
    missing = []
    for b in merged_files:
        p = find_clip(b)
        if p:
            clip_paths.append(p)
        else:
            missing.append(b)

    if missing:
        print('Missing source clips: ' + ', '.join(missing))
        sys.exit(4)

    os.makedirs(MERGED_ROOT, exist_ok=True)
    base, ext = os.path.splitext(TARGET_BASENAME)
    out_path = os.path.join(MERGED_ROOT, base + '_fixed' + ext)

    print(f'Re-merging {len(clip_paths)} clips -> {out_path}')

    merger = VideoMerger(ACCOUNT)
    ok = merger.merge_videos_with_normalization(clip_paths, out_path)
    if ok:
        size_mb = os.path.getsize(out_path) / (1024*1024)
        print(f'SUCCESS: {out_path} ({size_mb:.1f}MB)')
        sys.exit(0)
    else:
        print('FAILED to re-merge')
        sys.exit(5)


if __name__ == '__main__':
    main()
