# tkinter: GUI를 만들기 위한 파이썬 표준 라이브러리
import tkinter as tk

# messagebox: 알림창, 오류창 등 메시지를 띄울 때 사용
# scrolledtext: 스크롤 가능한 텍스트 박스를 만들 때 사용
from tkinter import messagebox, scrolledtext

# yt_dlp: 유튜브 영상 다운로드를 위한 강력한 라이브러리
from yt_dlp import YoutubeDL

# threading: 다운로드 중에도 GUI가 멈추지 않게 하기 위해 사용
import threading


# 사용자가 "다운로드" 버튼을 클릭했을 때 실행되는 함수
def download_video():
    url = url_entry.get()  # 입력창에서 사용자가 입력한 URL 가져오기
    if not url:  # URL이 비어 있으면
        messagebox.showwarning("입력 오류", "URL을 입력해주세요.")  # 경고창 띄우기
        return  # 함수 종료

    # 로그 창 초기화: 이전에 있던 텍스트 지우기
    log_text.configure(state='normal')  # 텍스트 편집 가능 상태로 전환
    log_text.delete('1.0', tk.END)      # 텍스트 전체 삭제
    log_text.configure(state='disabled')  # 다시 읽기 전용으로 전환

    # 다운로드를 새로운 스레드에서 실행 (그래야 창이 멈추지 않음)
    threading.Thread(target=run_download, args=(url,), daemon=True).start()


# 실질적으로 다운로드를 실행하는 함수
def run_download(url):
    # 다운로드 중간중간 호출되는 콜백 함수
    def progress_hook(d):
        if d['status'] == 'downloading':  # 현재 다운로드 중이면
            percent = d.get('_percent_str', '').strip()  # 다운로드 퍼센트
            speed = d.get('_speed_str', '').strip()      # 속도
            eta = d.get('_eta_str', '').strip()          # 예상 남은 시간
            msg = f"다운로드 중: {percent} @ {speed}, 남은 시간: {eta}"
        elif d['status'] == 'finished':  # 다운로드가 끝났으면
            msg = "다운로드 완료!"
        else:  # 기타 상태 처리
            msg = f"상태: {d['status']}"

        # 메시지를 GUI 로그창에 표시 (메인 쓰레드에서 실행되도록 .after 사용)
        log_text.after(0, append_log, msg)

    # yt-dlp 설정값
    ydl_opts = {
        'format': 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]',  # 1080p 이하 영상 + m4a 오디오
        'merge_output_format': 'mp4',       # 비디오 + 오디오를 mp4 파일로 병합
        'outtmpl': '%(title)s.%(ext)s',     # 저장되는 파일 이름: 유튜브 영상 제목.확장자
        'progress_hooks': [progress_hook],  # 다운로드 진행 상태를 알려주는 훅 함수
        'quiet': True,                      # 기본 로그 출력 안함
        'no_warnings': True,                # 경고 메시지도 출력 안함
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:  # 위 설정으로 yt-dlp 객체 생성
            ydl.download([url])          # 유튜브 URL 다운로드 실행

        # 완료 메시지를 GUI에 표시
        log_text.after(0, lambda: messagebox.showinfo("완료", "다운로드가 완료되었습니다."))
    except Exception as e:
        # 오류 발생 시 GUI에 에러 메시지 표시
        log_text.after(0, lambda: messagebox.showerror("오류", f"다운로드 중 오류가 발생했습니다:\n{e}"))

# 로그 메시지를 GUI 창에 추가하는 함수
def append_log(message):
    log_text.configure(state='normal')         # 편집 가능 상태로 변경
    log_text.insert(tk.END, message + '\n')    # 메시지 추가
    log_text.see(tk.END)                       # 가장 아래로 자동 스크롤
    log_text.configure(state='disabled')       # 다시 읽기 전용으로 변경

# 메인 창 생성
root = tk.Tk()
root.title("YouTube 영상 다운로드기")  # 창 제목 설정

# URL 입력창 라벨
tk.Label(root, text="YouTube URL:").pack(pady=5)  # 안내 문구
# URL 입력창 (가로 길이 50글자)
url_entry = tk.Entry(root, width=50)  # URL 입력창
url_entry.pack(pady=5)

# 다운로드 버튼
download_button = tk.Button(root, text="다운로드", command=download_video)  # 다운로드 버튼
download_button.pack(pady=10)

# 다운로드 로그 출력창 (스크롤 가능한 텍스트 박스)
log_text = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled')  # 로그 출력 창
log_text.pack(padx=10, pady=10)

# 이벤트 루프 실행: 창을 띄우고 사용자 입력 대기
root.mainloop()  # GUI 시작
