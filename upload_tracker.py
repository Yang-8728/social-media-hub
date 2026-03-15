"""
上传记录管理 - 追踪已上传的视频编号
"""
import json
from pathlib import Path
from datetime import datetime

UPLOAD_RECORD_FILE = "videos/upload_history.json"

def load_upload_history():
    """加载上传历史"""
    record_file = Path(UPLOAD_RECORD_FILE)
    if record_file.exists():
        with open(record_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"ai_vanvan": {"last_number": 123, "uploads": []}}

def save_upload_history(history):
    """保存上传历史"""
    record_file = Path(UPLOAD_RECORD_FILE)
    record_file.parent.mkdir(parents=True, exist_ok=True)
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_next_number(account="ai_vanvan"):
    """获取下一个视频编号"""
    history = load_upload_history()
    if account not in history:
        history[account] = {"last_number": 123, "uploads": []}
    return history[account]["last_number"] + 1

def record_upload(account, number, bv_id=None, title=None):
    """记录上传"""
    history = load_upload_history()
    if account not in history:
        history[account] = {"last_number": 123, "uploads": []}
    
    # 更新最大编号
    if number > history[account]["last_number"]:
        history[account]["last_number"] = number
    
    # 添加上传记录
    upload_record = {
        "number": number,
        "title": title or f"ins海外离大谱#{number}",
        "bv_id": bv_id,
        "upload_time": datetime.now().isoformat(),
        "status": "uploaded"
    }
    history[account]["uploads"].append(upload_record)
    
    save_upload_history(history)
    return upload_record

def mark_deleted(account, number):
    """标记视频已删除（但不减少编号）"""
    history = load_upload_history()
    if account in history:
        for upload in history[account]["uploads"]:
            if upload["number"] == number:
                upload["status"] = "deleted"
                upload["delete_time"] = datetime.now().isoformat()
        save_upload_history(history)

if __name__ == "__main__":
    # 初始化/检查上传历史
    history = load_upload_history()
    
    print("=" * 70)
    print("上传历史记录")
    print("=" * 70)
    
    for account, data in history.items():
        print(f"\n账号: {account}")
        print(f"当前最大编号: #{data['last_number']}")
        print(f"下一个编号: #{data['last_number'] + 1}")
        print(f"\n最近上传:")
        
        recent_uploads = sorted(data['uploads'], key=lambda x: x['number'], reverse=True)[:5]
        for upload in recent_uploads:
            status_icon = "✅" if upload['status'] == 'uploaded' else "❌"
            print(f"  {status_icon} #{upload['number']:3d} - {upload.get('title', 'N/A')}")
            if upload.get('bv_id'):
                print(f"      BV: {upload['bv_id']}")
