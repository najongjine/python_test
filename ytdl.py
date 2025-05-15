# pip install yt_dlp

from yt_dlp import YoutubeDL

def download_video(url):
    ydl_opts = {
        'format': 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

url="https://www.youtube.com/watch?v=MAdq_B4_4_w"
download_video(url)
