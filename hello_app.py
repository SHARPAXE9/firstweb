#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import datetime

class HelloApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("안녕하세요 앱")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # 배경색 설정
        self.window.configure(bg='#f0f0f0')
        
        self.create_widgets()
        
    def create_widgets(self):
        # 제목 라벨
        title_label = tk.Label(
            self.window,
            text="파이썬 실행파일 데모",
            font=("맑은 고딕", 20, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # 현재 시간 표시
        current_time = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
        time_label = tk.Label(
            self.window,
            text=f"현재 시간: {current_time}",
            font=("맑은 고딕", 12),
            bg='#f0f0f0',
            fg='#666666'
        )
        time_label.pack(pady=10)
        
        # 입력 필드
        self.name_var = tk.StringVar()
        name_frame = tk.Frame(self.window, bg='#f0f0f0')
        name_frame.pack(pady=20)
        
        tk.Label(
            name_frame,
            text="이름을 입력하세요:",
            font=("맑은 고딕", 12),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=5)
        
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=("맑은 고딕", 12),
            width=15
        )
        name_entry.pack(side=tk.LEFT, padx=5)
        
        # 버튼들
        button_frame = tk.Frame(self.window, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        hello_btn = tk.Button(
            button_frame,
            text="인사하기",
            font=("맑은 고딕", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            width=10,
            command=self.say_hello
        )
        hello_btn.pack(side=tk.LEFT, padx=10)
        
        time_btn = tk.Button(
            button_frame,
            text="시간 업데이트",
            font=("맑은 고딕", 12, "bold"),
            bg='#2196F3',
            fg='white',
            width=12,
            command=self.update_time
        )
        time_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(
            button_frame,
            text="종료",
            font=("맑은 고딕", 12, "bold"),
            bg='#f44336',
            fg='white',
            width=8,
            command=self.window.quit
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # 결과 표시 라벨
        self.result_label = tk.Label(
            self.window,
            text="",
            font=("맑은 고딕", 14, "bold"),
            bg='#f0f0f0',
            fg='#4CAF50'
        )
        self.result_label.pack(pady=20)
        
        # 저장된 시간 라벨
        self.time_label = time_label
        
    def say_hello(self):
        name = self.name_var.get().strip()
        if name:
            message = f"안녕하세요, {name}님! 👋"
            self.result_label.config(text=message)
            messagebox.showinfo("인사", message)
        else:
            messagebox.showwarning("경고", "이름을 입력해주세요!")
            
    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
        self.time_label.config(text=f"현재 시간: {current_time}")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = HelloApp()
    app.run()
