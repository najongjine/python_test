import tkinter as tk
from tkinter import messagebox, scrolledtext
from yt_dlp import YoutubeDL
import threading

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("입력 오류", "URL을 입력해주세요.")
        return

    # 로그 텍스트 위젯을 초기화
    log_text.configure(state='normal')
    log_text.delete('1.0', tk.END)
    log_text.configure(state='disabled')

    # 다운로드를 별도의 스레드에서 실행하여 GUI 응답성을 유지
    threading.Thread(target=run_download, args=(url,), daemon=True).start()

def run_download(url):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            msg = f"다운로드 중: {percent} @ {speed}, 남은 시간: {eta}"
        elif d['status'] == 'finished':
            msg = "다운로드 완료!"
        else:
            msg = f"상태: {d['status']}"

        # GUI에서 로그를 업데이트
        log_text.after(0, append_log, msg)

    ydl_opts = {
        'format': 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        log_text.after(0, lambda: messagebox.showinfo("완료", "다운로드가 완료되었습니다."))
    except Exception as e:
        log_text.after(0, lambda: messagebox.showerror("오류", f"다운로드 중 오류가 발생했습니다:\n{e}"))

def append_log(message):
    log_text.configure(state='normal')
    log_text.insert(tk.END, message + '\n')
    log_text.see(tk.END)
    log_text.configure(state='disabled')

# GUI 설정
root = tk.Tk()
root.title("YouTube 영상 다운로드기")

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="다운로드", command=download_video)
download_button.pack(pady=10)

# 로그 출력용 ScrolledText 위젯 추가
log_text = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled')
log_text.pack(padx=10, pady=10)

root.mainloop()
