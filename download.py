import yt_dlp
import os

# Get video URL from environment variable or use default
video_url = os.environ.get('VIDEO_URL', 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID')

# Set your desired output folder
output_folder = "downloads"

# Create folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Hook function to show progress
def progress_hook(d):
    if d['status'] == 'downloading':
        if not getattr(progress_hook, 'started', False):
            print(f"\n📥 Starting download: {d.get('filename', '')}")
            progress_hook.started = True
    elif d['status'] == 'finished':
        print(f"\n✅ Download finished: {d.get('filename', '')}")
progress_hook.started = False

# yt-dlp options - prioritizes 1080p, but doesn't force if unavailable
ydl_opts = {
    'format': 'bestvideo[height<=1080][height>=720]+bestaudio/best[height<=1080]',
    'merge_output_format': 'mp4',
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'progress_hooks': [progress_hook],
    'noplaylist': True,
    'quiet': False,
}

# Download
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("\n🎉 Download completed successfully!")
except Exception as e:
    print(f"\n❌ Error downloading video: {e}")
    exit(1)
