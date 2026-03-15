"""
标记所有现有的 YouTube 点赞为"已下载"
这样程序只会下载从现在开始新点赞的视频
"""
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# YouTube API 权限范围
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def mark_all_as_downloaded():
    """标记所有现有点赞为已下载"""
    print("🔍 开始获取所有现有的 YouTube 点赞...")
    
    # 加载 token
    token_file = "temp/youtube_youtube_token.json"
    if not os.path.exists(token_file):
        print("❌ 未找到 YouTube token 文件，请先运行一次下载命令进行认证")
        return
    
    # 加载凭据
    credentials = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # 刷新 token（如果需要）
    if credentials.expired and credentials.refresh_token:
        print("🔄 刷新 token...")
        credentials.refresh(Request())
    
    # 创建 YouTube API 客户端
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # 获取所有点赞的视频 ID
    all_video_ids = []
    page_token = None
    page_count = 0
    
    print("📥 正在获取点赞列表...")
    
    while True:
        page_count += 1
        print(f"   处理第 {page_count} 页...")
        
        # 获取点赞列表
        request = youtube.videos().list(
            part='id',
            myRating='like',
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()
        
        if not response.get('items'):
            break
        
        # 收集视频 ID
        for item in response['items']:
            video_id = item['id']
            all_video_ids.append(video_id)
        
        print(f"   已收集 {len(all_video_ids)} 个视频 ID...")
        
        # 检查是否还有下一页
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    
    print(f"\n✅ 共找到 {len(all_video_ids)} 个点赞视频")
    
    if len(all_video_ids) == 0:
        print("ℹ️ 没有需要标记的视频")
        return
    
    # 创建标记文件
    marker_dir = "videos/downloads/youtube"
    os.makedirs(marker_dir, exist_ok=True)
    
    marker_file = os.path.join(marker_dir, ".downloaded_marker.txt")
    
    print(f"\n📝 正在写入标记文件: {marker_file}")
    
    with open(marker_file, 'w', encoding='utf-8') as f:
        for video_id in all_video_ids:
            f.write(f"{video_id}\n")
    
    print(f"✅ 成功标记 {len(all_video_ids)} 个视频为已下载")
    print(f"\n💡 从现在开始，只有新点赞的视频才会被下载")
    print(f"🎯 你可以运行以下命令测试：")
    print(f"   python main.py --download --youtube")

if __name__ == "__main__":
    mark_all_as_downloaded()
