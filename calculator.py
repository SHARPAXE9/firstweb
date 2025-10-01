#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("계산기")
        self.window.geometry("320x450")
        self.window.resizable(False, False)
        self.window.configure(bg='#8B0000')  # 다크 레드 배경
        
        # 계산 상태 변수들
        self.current = "0"
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False
        
        self.create_display()
        self.create_buttons()
        
    def create_display(self):
        """디스플레이 화면 생성"""
        self.display_frame = tk.Frame(self.window, bg='#8B0000')
        self.display_frame.pack(expand=False, fill="both", padx=10, pady=(10, 5))
        
        self.display = tk.Label(
            self.display_frame,
            text=self.current,
            anchor=tk.E,
            bg='#2F0000',  # 매우 어두운 빨간색
            fg='#FFE4E1',  # 연한 핑크색 텍스트
            font=('Arial', 24, 'bold'),
            height=2,
            relief='sunken',
            bd=2
        )
        self.display.pack(expand=True, fill="both", padx=5, pady=5)
        
    def create_buttons(self):
        """버튼들 생성 및 배치"""
        self.button_frame = tk.Frame(self.window, bg='#8B0000')
        self.button_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        # 그리드 가중치 설정
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        
        # 버튼 정의 (행, 열, 텍스트, 배경색, 전경색, 행스팬, 열스팬) - 빨간색 테마
        buttons = [
            # 첫 번째 행
            (0, 0, "C", "#DC143C", "white", 1, 1),      # 크림슨 레드
            (0, 1, "±", "#B22222", "white", 1, 1),      # 파이어브릭
            (0, 2, "%", "#B22222", "white", 1, 1),      # 파이어브릭
            (0, 3, "÷", "#FF4500", "white", 1, 1),      # 오렌지레드
            
            # 두 번째 행
            (1, 0, "7", "#8B0000", "#FFE4E1", 1, 1),   # 다크레드 배경, 연한 핑크 텍스트
            (1, 1, "8", "#8B0000", "#FFE4E1", 1, 1),
            (1, 2, "9", "#8B0000", "#FFE4E1", 1, 1),
            (1, 3, "×", "#FF4500", "white", 1, 1),      # 오렌지레드
            
            # 세 번째 행
            (2, 0, "4", "#8B0000", "#FFE4E1", 1, 1),
            (2, 1, "5", "#8B0000", "#FFE4E1", 1, 1),
            (2, 2, "6", "#8B0000", "#FFE4E1", 1, 1),
            (2, 3, "-", "#FF4500", "white", 1, 1),      # 오렌지레드
            
            # 네 번째 행
            (3, 0, "1", "#8B0000", "#FFE4E1", 1, 1),
            (3, 1, "2", "#8B0000", "#FFE4E1", 1, 1),
            (3, 2, "3", "#8B0000", "#FFE4E1", 1, 1),
            (3, 3, "+", "#FF4500", "white", 1, 1),      # 오렌지레드
            
            # 다섯 번째 행
            (4, 0, "0", "#8B0000", "#FFE4E1", 1, 2),   # 0은 2칸 차지
            (4, 2, ".", "#8B0000", "#FFE4E1", 1, 1),
            (4, 3, "=", "#FF6347", "white", 1, 1),      # 토마토 레드
        ]
        
        # 버튼 생성 및 배치
        for row, col, text, bg_color, fg_color, rowspan, colspan in buttons:
            btn = tk.Button(
                self.button_frame,
                text=text,
                bg=bg_color,
                fg=fg_color,
                font=('Arial', 18, 'bold'),
                relief='raised',
                bd=2,
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(
                row=row, 
                column=col, 
                rowspan=rowspan, 
                columnspan=colspan,
                sticky="nsew", 
                padx=2, 
                pady=2
            )
            
            # 버튼 호버 효과
            self.add_hover_effect(btn, bg_color)
    
    def add_hover_effect(self, button, original_color):
        """버튼 호버 효과 추가"""
        def on_enter(e):
            button.configure(bg=self.lighten_color(original_color))
        
        def on_leave(e):
            button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        """색상을 밝게 만드는 함수 - 빨간색 테마용"""
        color_map = {
            "#DC143C": "#FF1493",  # 크림슨 -> 딥핑크
            "#B22222": "#DC143C",  # 파이어브릭 -> 크림슨
            "#FF4500": "#FF6347",  # 오렌지레드 -> 토마토
            "#8B0000": "#B22222",  # 다크레드 -> 파이어브릭
            "#FF6347": "#FF7F7F"   # 토마토 -> 연한 토마토
        }
        return color_map.get(color, color)
    
    def button_click(self, char):
        """버튼 클릭 이벤트 처리"""
        if self.result == True:
            self.current = "0"
            self.result = False
        
        if char in "0123456789":
            self.number_press(char)
        elif char == ".":
            self.decimal_press()
        elif char in "+-×÷":
            self.operation_press(char)
        elif char == "=":
            self.equal_press()
        elif char == "C":
            self.clear_press()
        elif char == "±":
            self.sign_press()
        elif char == "%":
            self.percent_press()
    
    def number_press(self, num):
        """숫자 버튼 처리"""
        if self.input_value:
            self.current = num
            self.input_value = False
        else:
            if self.current == "0":
                self.current = num
            else:
                self.current += num
        self.display.config(text=self.current)
    
    def decimal_press(self):
        """소수점 버튼 처리"""
        if self.input_value:
            self.current = "0."
            self.input_value = False
        else:
            if "." not in self.current:
                self.current += "."
        self.display.config(text=self.current)
    
    def operation_press(self, op):
        """연산자 버튼 처리"""
        if self.current == "Error":
            return
            
        if self.check_sum:
            self.equal_press()
        
        if not self.result:
            self.total = float(self.current)
            self.result = True
        
        self.check_sum = True
        self.op = op
        self.input_value = True
    
    def equal_press(self):
        """등호 버튼 처리"""
        if self.op == "" or self.current == "Error":
            return
        
        try:
            if self.op == "+":
                self.total += float(self.current)
            elif self.op == "-":
                self.total -= float(self.current)
            elif self.op == "×":
                self.total *= float(self.current)
            elif self.op == "÷":
                if float(self.current) == 0:
                    self.current = "Error"
                    self.display.config(text=self.current)
                    return
                self.total /= float(self.current)
            
            # 결과가 정수인지 확인
            if self.total == int(self.total):
                self.current = str(int(self.total))
            else:
                self.current = str(round(self.total, 10))
                # 불필요한 0 제거
                if '.' in self.current:
                    self.current = self.current.rstrip('0').rstrip('.')
            
        except:
            self.current = "Error"
        
        self.display.config(text=self.current)
        self.check_sum = False
        self.input_value = True
        self.result = False
    
    def clear_press(self):
        """클리어 버튼 처리"""
        self.current = "0"
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False
        self.display.config(text=self.current)
    
    def sign_press(self):
        """부호 변경 버튼 처리"""
        if self.current == "0" or self.current == "Error":
            return
        
        if self.current[0] == "-":
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current
        
        self.display.config(text=self.current)
    
    def percent_press(self):
        """퍼센트 버튼 처리"""
        if self.current == "Error":
            return
        
        try:
            result = float(self.current) / 100
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(result)
            self.display.config(text=self.current)
        except:
            self.current = "Error"
            self.display.config(text=self.current)
    
    def run(self):
        """계산기 실행"""
        # 키보드 이벤트 바인딩
        self.window.bind('<Key>', self.key_press)
        self.window.focus_set()
        self.window.mainloop()
    
    def key_press(self, event):
        """키보드 입력 처리"""
        key = event.char
        if key in "0123456789.":
            self.button_click(key)
        elif key in "+-":
            self.button_click(key)
        elif key == "*":
            self.button_click("×")
        elif key == "/":
            self.button_click("÷")
        elif key in "\r\n=":  # Enter 키
            self.button_click("=")
        elif key in "\x08\x7f":  # Backspace 또는 Delete
            if len(self.current) > 1:
                self.current = self.current[:-1]
            else:
                self.current = "0"
            self.display.config(text=self.current)
        elif key.lower() == "c":
            self.button_click("C")

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
