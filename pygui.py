import tkinter as tk
from tkinter import scrolledtext

def on_button_click():
    log_text.configure(state='normal')  # 텍스트 위젯을 수정 가능 상태로 변경
    log_text.insert(tk.END, "버튼이 클릭되었습니다.\n")  # 메시지 추가
    log_text.configure(state='disabled')  # 텍스트 위젯을 수정 불가능 상태로 변경
    log_text.yview(tk.END)  # 스크롤을 가장 아래로 이동

root = tk.Tk()
root.title("로그 출력 GUI 예제")

# ScrolledText 위젯 생성
log_text = scrolledtext.ScrolledText(root, width=50, height=10, state='disabled')
log_text.pack(padx=10, pady=10)

# 버튼 생성
button = tk.Button(root, text="클릭하세요", command=on_button_click)
button.pack(pady=5)

root.mainloop()
