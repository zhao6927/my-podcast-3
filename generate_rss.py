import os
import time
from urllib.parse import quote
from feedgen.feed import FeedGenerator

# --- 核心配置 ---
TARGET_FOLDER = "播客"
BASE_URL = "https://zhao6927.github.io/my-podcast-3/" 
AUDIO_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.aac', '.mp4')
RSS_FILENAME = "podcast.xml"
# 确保你在根目录下上传了 logo.jpg
GLOBAL_IMAGE = f"{BASE_URL}logo.jpg" 

def generate_rss():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    
    # --- 频道全局设置 ---
    fg.title('谈怪谈')
    fg.author({'name': '您的名字'})
    fg.description('自动扫描“播客”文件夹生成的订阅源')
    fg.link(href=BASE_URL, rel='alternate')
    fg.language('zh-CN')
    
    # 强制设置全局主图（给频道）
    fg.image(GLOBAL_IMAGE)
    fg.podcast.itunes_image(GLOBAL_IMAGE)

    if not os.path.exists(TARGET_FOLDER):
        print(f"找不到文件夹: {TARGET_FOLDER}")
        return

    files_to_process = []
    for f in os.listdir(TARGET_FOLDER):
        if f.lower().endswith(AUDIO_EXTENSIONS):
            full_path = os.path.join(TARGET_FOLDER, f)
            files_to_process.append((full_path, f))

    files_to_process.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)

    for full_path, filename in files_to_process:
        fe = fg.add_entry()
        fe.title(filename.rsplit('.', 1)[0]) 
        
        # 强制设置每一集的图片为全局主图（覆盖内封图显示）
        fe.podcast.itunes_image(GLOBAL_IMAGE)
        
        encoded_path = quote(f"{TARGET_FOLDER}/{filename}")
        file_url = f"{BASE_URL}{encoded_path}"
        
        fe.enclosure(file_url, str(os.path.getsize(full_path)), 'audio/mpeg')
        fe.guid(file_url)
        
        file_mtime = time.gmtime(os.path.getmtime(full_path))
        fe.pubDate(time.strftime('%a, %d %b %Y %H:%M:%S +0000', file_mtime))

    fg.rss_file(RSS_FILENAME)
    print("RSS 生成成功，已应用全局统一封面！")

if __name__ == "__main__":
    generate_rss()
