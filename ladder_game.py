#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class LadderGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("편가르기 사다리 게임")
        self.root.geometry("900x1000")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f8ff')
        
        # 게임 상태 변수들
        self.teams = []
        self.people = []
        self.ladder_lines = []
        self.canvas = None
        self.animation_running = False
        
        self.create_setup_frame()
        
    def create_setup_frame(self):
        """게임 설정 화면 생성"""
        self.setup_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.setup_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 제목
        title_label = tk.Label(
            self.setup_frame,
            text="🎯 편가르기 사다리 게임",
            font=('맑은 고딕', 24, 'bold'),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # 설정 프레임
        config_frame = tk.Frame(self.setup_frame, bg='#f0f8ff')
        config_frame.pack(pady=20)
        
        # 팀 개수 설정
        team_frame = tk.Frame(config_frame, bg='#f0f8ff')
        team_frame.pack(pady=10)
        
        tk.Label(
            team_frame,
            text="팀 개수:",
            font=('맑은 고딕', 14),
            bg='#f0f8ff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.team_count_var = tk.StringVar(value="2")
        team_spinbox = tk.Spinbox(
            team_frame,
            from_=2,
            to=6,
            width=5,
            textvariable=self.team_count_var,
            font=('맑은 고딕', 12),
            command=self.update_team_inputs
        )
        team_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 팀당 인원수 설정
        members_frame = tk.Frame(config_frame, bg='#f0f8ff')
        members_frame.pack(pady=10)
        
        tk.Label(
            members_frame,
            text="팀당 인원수:",
            font=('맑은 고딕', 14),
            bg='#f0f8ff'
        ).pack(side=tk.LEFT, padx=5)
        
        self.members_per_team_var = tk.StringVar(value="4")
        members_spinbox = tk.Spinbox(
            members_frame,
            from_=2,
            to=8,
            width=5,
            textvariable=self.members_per_team_var,
            font=('맑은 고딕', 12),
            command=self.update_team_inputs
        )
        members_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 참석자 명단 입력 프레임
        attendee_frame = tk.LabelFrame(
            self.setup_frame,
            text="📝 참석자 명단 입력",
            font=('맑은 고딕', 14, 'bold'),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        attendee_frame.pack(pady=20, padx=20, fill='x')
        
        # 참석자 명단 입력 안내
        tk.Label(
            attendee_frame,
            text="참석자 이름을 쉼표(,)로 구분하여 입력하세요:",
            font=('맑은 고딕', 12),
            bg='#f0f8ff'
        ).pack(pady=5)
        
        # 참석자 명단 입력 텍스트 박스
        self.attendee_text = tk.Text(
            attendee_frame,
            height=4,
            width=60,
            font=('맑은 고딕', 11),
            wrap=tk.WORD
        )
        self.attendee_text.pack(pady=5, padx=10)
        
        # 참석자 명단 버튼 프레임
        attendee_btn_frame = tk.Frame(attendee_frame, bg='#f0f8ff')
        attendee_btn_frame.pack(pady=10)
        
        random_attendee_btn = tk.Button(
            attendee_btn_frame,
            text="🎲 샘플 명단 생성",
            font=('맑은 고딕', 12, 'bold'),
            bg='#9b59b6',
            fg='white',
            width=15,
            command=self.generate_sample_attendees
        )
        random_attendee_btn.pack(side=tk.LEFT, padx=5)
        
        random_team_btn = tk.Button(
            attendee_btn_frame,
            text="🔀 랜덤 팀 배정",
            font=('맑은 고딕', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            width=15,
            command=self.random_team_assignment
        )
        random_team_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            attendee_btn_frame,
            text="🗑️ 명단 지우기",
            font=('맑은 고딕', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            width=15,
            command=self.clear_attendees
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 팀 배정 결과 표시 프레임
        self.result_frame = tk.LabelFrame(
            self.setup_frame,
            text="🏆 팀 배정 결과",
            font=('맑은 고딕', 14, 'bold'),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        # 처음에는 숨김
        
        # 스크롤바와 함께 텍스트 위젯 생성
        result_scroll_frame = tk.Frame(self.result_frame, bg='#f0f8ff')
        
        self.result_text = tk.Text(
            result_scroll_frame,
            height=10,
            width=70,
            font=('맑은 고딕', 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg='#ffffff'
        )
        
        # 스크롤바 추가
        result_scrollbar = tk.Scrollbar(result_scroll_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        # 스크롤바와 텍스트 위젯 배치
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 스크롤 프레임을 결과 프레임에 패킹 (나중에 사용)
        self.result_scroll_frame = result_scroll_frame
        
        # 인원 입력 프레임
        self.people_frame = tk.Frame(self.setup_frame, bg='#f0f8ff')
        self.people_frame.pack(pady=20)
        
        self.people_entries = []
        self.update_team_inputs()
        
        # 버튼 프레임
        button_frame = tk.Frame(self.setup_frame, bg='#f0f8ff')
        button_frame.pack(pady=30)
        
        start_btn = tk.Button(
            button_frame,
            text="🎮 사다리 게임 시작",
            font=('맑은 고딕', 16, 'bold'),
            bg='#3498db',
            fg='white',
            width=20,
            height=2,
            command=self.start_game
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        
        random_btn = tk.Button(
            button_frame,
            text="🎲 랜덤 생성",
            font=('맑은 고딕', 16, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=15,
            height=2,
            command=self.generate_random_names
        )
        random_btn.pack(side=tk.LEFT, padx=10)
        
    def update_team_inputs(self):
        """팀 개수와 팀당 인원수에 따라 인원 입력 필드 업데이트"""
        # 기존 입력 필드 제거
        for widget in self.people_frame.winfo_children():
            widget.destroy()
        
        self.people_entries = []
        team_count = int(self.team_count_var.get())
        members_per_team = int(self.members_per_team_var.get())
        
        tk.Label(
            self.people_frame,
            text="참가자 이름을 입력하세요:",
            font=('맑은 고딕', 14, 'bold'),
            bg='#f0f8ff'
        ).pack(pady=10)
        
        # 팀별 색상
        team_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        for i in range(team_count):
            team_frame = tk.LabelFrame(
                self.people_frame,
                text=f"팀 {i+1} ({members_per_team}명)",
                font=('맑은 고딕', 12, 'bold'),
                bg='#f0f8ff',
                fg=team_colors[i % len(team_colors)]
            )
            team_frame.pack(pady=5, padx=20, fill='x')
            
            entry_frame = tk.Frame(team_frame, bg='#f0f8ff')
            entry_frame.pack(pady=10)
            
            team_entries = []
            for j in range(members_per_team):  # 설정된 팀당 인원수만큼
                entry = tk.Entry(
                    entry_frame,
                    font=('맑은 고딕', 11),
                    width=12,
                    justify='center'
                )
                entry.pack(side=tk.LEFT, padx=2)
                team_entries.append(entry)
            
            self.people_entries.append(team_entries)
    
    def generate_random_names(self):
        """랜덤 이름 생성"""
        sample_names = [
            "김철수", "이영희", "박민수", "최지은", "정다은", "한승우",
            "오지훈", "임수빈", "윤서연", "장현우", "조민지", "강태현",
            "신예린", "배준호", "송하늘", "류지민", "홍서준", "문채원",
            "노은우", "서지안", "권민석", "양수진", "천하람", "표준영",
            "이도현", "김서윤", "박지호", "최민아", "정우진", "한소영",
            "오태민", "임지우", "윤하은", "장민준", "조서현", "강예준"
        ]
        
        team_count = int(self.team_count_var.get())
        members_per_team = int(self.members_per_team_var.get())
        used_names = set()
        
        for i in range(team_count):
            for j in range(members_per_team):
                if j < len(self.people_entries[i]):
                    available_names = [name for name in sample_names if name not in used_names]
                    if available_names:
                        name = random.choice(available_names)
                        used_names.add(name)
                        self.people_entries[i][j].delete(0, tk.END)
                        self.people_entries[i][j].insert(0, name)
    
    def generate_sample_attendees(self):
        """샘플 참석자 명단 생성"""
        sample_names = [
            "김철수", "이영희", "박민수", "최지은", "정다은", "한승우",
            "오지훈", "임수빈", "윤서연", "장현우", "조민지", "강태현",
            "신예린", "배준호", "송하늘", "류지민", "홍서준", "문채원",
            "노은우", "서지안", "권민석", "양수진", "천하람", "표준영",
            "이도현", "김서윤", "박지호", "최민아", "정우진", "한소영"
        ]
        
        # 랜덤하게 12-20명 선택
        num_people = random.randint(12, 20)
        selected_names = random.sample(sample_names, min(num_people, len(sample_names)))
        
        # 텍스트 박스에 입력
        self.attendee_text.delete(1.0, tk.END)
        self.attendee_text.insert(1.0, ", ".join(selected_names))
    
    def clear_attendees(self):
        """참석자 명단 지우기"""
        self.attendee_text.delete(1.0, tk.END)
        # 팀 입력 필드도 초기화
        for team_entries in self.people_entries:
            for entry in team_entries:
                entry.delete(0, tk.END)
        # 결과 프레임 숨기기
        self.hide_result_frame()
    
    def random_team_assignment(self):
        """랜덤 팀 배정 - 사다리 애니메이션과 함께"""
        # 참석자 명단 가져오기
        attendee_text = self.attendee_text.get(1.0, tk.END).strip()
        if not attendee_text:
            messagebox.showwarning("경고", "참석자 명단을 먼저 입력해주세요!")
            return
        
        # 이름 파싱
        attendees = [name.strip() for name in attendee_text.split(',') if name.strip()]
        if len(attendees) < 2:
            messagebox.showwarning("경고", "최소 2명 이상의 참석자가 필요합니다!")
            return
        
        team_count = int(self.team_count_var.get())
        members_per_team = int(self.members_per_team_var.get())
        
        # 필요한 총 인원수 계산
        total_needed = team_count * members_per_team
        
        if len(attendees) < total_needed:
            messagebox.showwarning(
                "경고", 
                f"참석자가 부족합니다!\n필요: {total_needed}명, 현재: {len(attendees)}명"
            )
            return
        
        # 사다리 애니메이션 창 열기
        self.show_ladder_animation_for_teams(attendees[:total_needed])
    
    def show_ladder_animation_for_teams(self, attendees):
        """팀 배정을 위한 사다리 애니메이션 표시"""
        # 새 창 생성
        self.ladder_window = tk.Toplevel(self.window)
        self.ladder_window.title("🎯 사다리 타기 - 팀 배정")
        self.ladder_window.geometry("800x600")
        self.ladder_window.configure(bg='#f0f8ff')
        self.ladder_window.grab_set()  # 모달 창으로 설정
        
        # 제목
        title_label = tk.Label(
            self.ladder_window,
            text="🎯 사다리 타기로 팀 배정 중...",
            font=('맑은 고딕', 18, 'bold'),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # 캔버스 생성
        self.ladder_canvas = tk.Canvas(
            self.ladder_window,
            bg='white',
            relief='raised',
            bd=2,
            width=750,
            height=450
        )
        self.ladder_canvas.pack(pady=10, padx=25)
        
        # 참석자와 팀 정보 저장
        self.current_attendees = attendees
        self.team_count = int(self.team_count_var.get())
        self.members_per_team = int(self.members_per_team_var.get())
        
        # 사다리 그리기 시작
        self.ladder_window.after(500, self.draw_team_ladder)
    
    def draw_team_ladder(self):
        """팀 배정용 사다리 그리기"""
        self.ladder_canvas.delete("all")
        
        canvas_width = 750
        canvas_height = 450
        people_count = len(self.current_attendees)
        
        # 사다리 기본 설정
        margin = 50
        ladder_width = canvas_width - 2 * margin
        ladder_height = canvas_height - 120
        
        # 세로선 간격
        if people_count > 1:
            line_spacing = ladder_width / (people_count - 1)
        else:
            line_spacing = ladder_width
        
        # 참가자 이름 표시 (상단)
        for i, person in enumerate(self.current_attendees):
            x = margin + i * line_spacing
            
            # 상단 이름
            self.ladder_canvas.create_text(
                x, 30,
                text=person,
                font=('맑은 고딕', 10, 'bold'),
                fill='#2c3e50'
            )
            
            # 세로선
            self.ladder_canvas.create_line(
                x, 50, x, 50 + ladder_height,
                fill='#34495e',
                width=3,
                tags="vertical_line"
            )
        
        # 팀 결과 표시 영역 (하단)
        team_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        team_y = 50 + ladder_height + 20
        
        # 팀 구분선 그리기
        team_width = ladder_width / self.team_count
        for i in range(self.team_count):
            color = team_colors[i % len(team_colors)]
            x_start = margin + i * team_width
            x_end = margin + (i + 1) * team_width
            
            # 팀 영역 배경
            self.ladder_canvas.create_rectangle(
                x_start, team_y - 10, x_end, team_y + 30,
                fill=color,
                outline=color,
                stipple='gray25',
                tags="team_area"
            )
            
            # 팀 라벨
            self.ladder_canvas.create_text(
                (x_start + x_end) / 2, team_y + 10,
                text=f"팀 {i+1}",
                font=('맑은 고딕', 12, 'bold'),
                fill='white',
                tags="team_label"
            )
        
        # 가로선 애니메이션 시작
        self.ladder_window.after(1000, self.animate_team_ladder)
    
    def animate_team_ladder(self):
        """팀 배정 사다리 애니메이션"""
        canvas_width = 750
        canvas_height = 450
        people_count = len(self.current_attendees)
        
        margin = 50
        ladder_width = canvas_width - 2 * margin
        ladder_height = canvas_height - 120
        
        if people_count > 1:
            line_spacing = ladder_width / (people_count - 1)
        else:
            line_spacing = ladder_width
        
        # 가로선 생성
        horizontal_lines = []
        num_levels = random.randint(8, 15)
        
        for level in range(num_levels):
            y = 70 + (level * (ladder_height - 40) / num_levels)
            
            # 각 레벨에서 랜덤하게 가로선 생성
            for i in range(people_count - 1):
                if random.random() < 0.4:  # 40% 확률로 가로선 생성
                    x1 = margin + i * line_spacing
                    x2 = margin + (i + 1) * line_spacing
                    horizontal_lines.append((x1, y, x2, y, i))
        
        # 가로선 애니메이션으로 그리기
        self.draw_team_lines_animated(horizontal_lines, 0)
    
    def draw_team_lines_animated(self, lines, index):
        """팀 배정용 가로선을 애니메이션으로 그리기"""
        if index >= len(lines):
            # 모든 선이 그려지면 결과 계산
            self.ladder_window.after(1000, self.calculate_team_result)
            return
        
        x1, y, x2, y2, connection = lines[index]
        
        # 가로선 그리기
        self.ladder_canvas.create_line(
            x1, y, x2, y2,
            fill='#e74c3c',
            width=4,
            tags="horizontal_line"
        )
        
        # 연결점 표시
        self.ladder_canvas.create_oval(
            x1-3, y-3, x1+3, y+3,
            fill='#c0392b',
            outline='#c0392b',
            tags="horizontal_line"
        )
        self.ladder_canvas.create_oval(
            x2-3, y2-3, x2+3, y2+3,
            fill='#c0392b',
            outline='#c0392b',
            tags="horizontal_line"
        )
        
        # 다음 선 그리기
        self.ladder_window.after(150, lambda: self.draw_team_lines_animated(lines, index + 1))
    
    def calculate_team_result(self):
        """팀 배정 결과 계산 및 표시"""
        canvas_width = 750
        people_count = len(self.current_attendees)
        
        margin = 50
        ladder_width = canvas_width - 2 * margin
        
        if people_count > 1:
            line_spacing = ladder_width / (people_count - 1)
        else:
            line_spacing = ladder_width
        
        # 각 사람의 경로 추적
        final_positions = list(range(people_count))
        
        # 가로선 정보 수집
        horizontal_connections = []
        for item in self.ladder_canvas.find_withtag("horizontal_line"):
            coords = self.ladder_canvas.coords(item)
            if len(coords) == 4:  # 선인 경우
                x1, y1, x2, y2 = coords
                pos1 = round((x1 - margin) / line_spacing)
                pos2 = round((x2 - margin) / line_spacing)
                if 0 <= pos1 < people_count and 0 <= pos2 < people_count:
                    horizontal_connections.append((y1, pos1, pos2))
        
        # y좌표 기준으로 정렬
        horizontal_connections.sort()
        
        # 경로 추적
        for y, pos1, pos2 in horizontal_connections:
            idx1 = final_positions.index(pos1)
            idx2 = final_positions.index(pos2)
            final_positions[idx1], final_positions[idx2] = final_positions[idx2], final_positions[idx1]
        
        # 팀 배정
        teams_result = []
        for i in range(self.team_count):
            team_members = []
            for j in range(self.members_per_team):
                person_idx = i * self.members_per_team + j
                if person_idx < len(final_positions):
                    original_person_idx = final_positions[person_idx]
                    team_members.append(self.current_attendees[original_person_idx])
            teams_result.append(team_members)
        
        # 결과를 메인 창에 적용
        self.apply_team_result(teams_result)
        
        # 결과 표시
        self.show_final_team_result(teams_result)
    
    def apply_team_result(self, teams_result):
        """계산된 팀 결과를 메인 창에 적용"""
        # 팀 입력 필드에 결과 적용
        for i, team_members in enumerate(teams_result):
            for j, member in enumerate(team_members):
                if i < len(self.people_entries) and j < len(self.people_entries[i]):
                    self.people_entries[i][j].delete(0, tk.END)
                    self.people_entries[i][j].insert(0, member)
        
        # 메인 창에 결과 표시
        self.show_team_assignment_result(teams_result)
    
    def show_final_team_result(self, teams_result):
        """사다리 창에서 최종 결과 표시"""
        # 결과 표시 영역
        result_y = 400
        
        # 배경
        self.ladder_canvas.create_rectangle(
            25, result_y, 725, 550,
            fill='#ecf0f1',
            outline='#bdc3c7',
            width=2,
            tags="final_result"
        )
        
        # 제목
        self.ladder_canvas.create_text(
            375, result_y + 20,
            text="🎉 팀 배정 완료! 🎉",
            font=('맑은 고딕', 16, 'bold'),
            fill='#2c3e50',
            tags="final_result"
        )
        
        # 팀별 결과
        team_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        for i, team_members in enumerate(teams_result):
            if team_members:
                color = team_colors[i % len(team_colors)]
                team_text = f"팀 {i+1}: {', '.join(team_members)}"
                
                self.ladder_canvas.create_text(
                    375, result_y + 50 + i * 25,
                    text=team_text,
                    font=('맑은 고딕', 12, 'bold'),
                    fill=color,
                    tags="final_result"
                )
        
        # 닫기 버튼
        close_btn = tk.Button(
            self.ladder_window,
            text="✅ 확인",
            font=('맑은 고딕', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            width=10,
            command=self.close_ladder_window
        )
        close_btn.pack(pady=10)
    
    def close_ladder_window(self):
        """사다리 창 닫기"""
        self.ladder_window.destroy()
    
    def show_team_assignment_result(self, teams_result):
        """팀 배정 결과 표시"""
        # 결과 프레임 표시
        self.result_frame.pack(pady=20, padx=20, fill='both', expand=True)
        self.result_scroll_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # 결과 텍스트 작성
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # 팀별 색상
        team_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        result_text = "🎯 랜덤 팀 배정 결과\n"
        result_text += "=" * 50 + "\n\n"
        
        for i, team_members in enumerate(teams_result):
            if team_members:
                result_text += f"🏆 팀 {i+1} ({len(team_members)}명)\n"
                result_text += f"   {', '.join(team_members)}\n\n"
        
        # 남은 참석자가 있는 경우
        total_assigned = sum(len(team) for team in teams_result)
        attendee_text = self.attendee_text.get(1.0, tk.END).strip()
        attendees = [name.strip() for name in attendee_text.split(',') if name.strip()]
        
        if len(attendees) > total_assigned:
            remaining = attendees[total_assigned:]
            result_text += f"⏳ 대기자 ({len(remaining)}명)\n"
            result_text += f"   {', '.join(remaining)}\n\n"
        
        result_text += "=" * 50 + "\n"
        result_text += f"총 참석자: {len(attendees)}명 | 배정 완료: {total_assigned}명"
        
        self.result_text.insert(1.0, result_text)
        self.result_text.config(state=tk.DISABLED)
    
    def hide_result_frame(self):
        """결과 프레임 숨기기"""
        self.result_frame.pack_forget()
    
    def start_game(self):
        """게임 시작"""
        # 입력 데이터 수집
        self.teams = []
        self.people = []
        
        for i, team_entries in enumerate(self.people_entries):
            team_members = []
            for entry in team_entries:
                name = entry.get().strip()
                if name:
                    team_members.append(name)
                    self.people.append(name)
            
            if team_members:
                self.teams.append(team_members)
        
        if len(self.people) < 2:
            messagebox.showwarning("경고", "최소 2명 이상의 참가자가 필요합니다!")
            return
        
        if len(self.teams) < 2:
            messagebox.showwarning("경고", "최소 2개 팀이 필요합니다!")
            return
        
        # 게임 화면으로 전환
        self.setup_frame.destroy()
        self.create_game_frame()
    
    def create_game_frame(self):
        """게임 화면 생성"""
        self.game_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.game_frame.pack(expand=True, fill='both')
        
        # 상단 제목
        title_frame = tk.Frame(self.game_frame, bg='#f0f8ff')
        title_frame.pack(pady=10)
        
        tk.Label(
            title_frame,
            text="🎯 편가르기 사다리 게임",
            font=('맑은 고딕', 20, 'bold'),
            bg='#f0f8ff',
            fg='#2c3e50'
        ).pack()
        
        # 캔버스 프레임
        canvas_frame = tk.Frame(self.game_frame, bg='#f0f8ff')
        canvas_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # 캔버스 생성
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            relief='raised',
            bd=2
        )
        self.canvas.pack(expand=True, fill='both')
        
        # 하단 버튼
        button_frame = tk.Frame(self.game_frame, bg='#f0f8ff')
        button_frame.pack(pady=10)
        
        draw_btn = tk.Button(
            button_frame,
            text="🎲 사다리 뽑기",
            font=('맑은 고딕', 14, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=15,
            command=self.draw_ladder
        )
        draw_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(
            button_frame,
            text="🔄 다시 설정",
            font=('맑은 고딕', 14, 'bold'),
            bg='#95a5a6',
            fg='white',
            width=15,
            command=self.reset_game
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        # 초기 사다리 그리기
        self.window.after(100, self.draw_initial_ladder)
    
    def draw_initial_ladder(self):
        """초기 사다리 그리기"""
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.window.after(100, self.draw_initial_ladder)
            return
        
        people_count = len(self.people)
        
        # 사다리 기본 설정
        margin = 80
        ladder_width = canvas_width - 2 * margin
        ladder_height = canvas_height - 150
        
        # 세로선 간격
        if people_count > 1:
            line_spacing = ladder_width / (people_count - 1)
        else:
            line_spacing = ladder_width
        
        # 참가자 이름 표시
        for i, person in enumerate(self.people):
            x = margin + i * line_spacing
            
            # 상단 이름
            self.canvas.create_text(
                x, 30,
                text=person,
                font=('맑은 고딕', 12, 'bold'),
                fill='#2c3e50'
            )
            
            # 세로선
            self.canvas.create_line(
                x, 50, x, 50 + ladder_height,
                fill='#34495e',
                width=3
            )
        
        # 팀 결과 표시 영역
        team_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        team_y = 50 + ladder_height + 30
        
        for i, team in enumerate(self.teams):
            color = team_colors[i % len(team_colors)]
            team_text = f"팀 {i+1}: {', '.join(team)}"
            
            self.canvas.create_text(
                canvas_width // 2, team_y + i * 25,
                text=team_text,
                font=('맑은 고딕', 11, 'bold'),
                fill=color
            )
    
    def draw_ladder(self):
        """사다리 뽑기 실행"""
        if self.animation_running:
            return
        
        self.animation_running = True
        
        # 기존 가로선 제거
        self.canvas.delete("horizontal_line")
        self.canvas.delete("result")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        people_count = len(self.people)
        
        margin = 80
        ladder_width = canvas_width - 2 * margin
        ladder_height = canvas_height - 150
        
        if people_count > 1:
            line_spacing = ladder_width / (people_count - 1)
        else:
            line_spacing = ladder_width
        
        # 가로선 생성
        horizontal_lines = []
        num_levels = random.randint(8, 15)  # 8-15개 레벨
        
        for level in range(num_levels):
            y = 70 + (level * (ladder_height - 40) / num_levels)
            
            # 각 레벨에서 랜덤하게 가로선 생성
            for i in range(people_count - 1):
                if random.random() < 0.4:  # 40% 확률로 가로선 생성
                    x1 = margin + i * line_spacing
                    x2 = margin + (i + 1) * line_spacing
                    
                    horizontal_lines.append((x1, y, x2, y, i))
        
        # 가로선 애니메이션으로 그리기
        self.draw_lines_animated(horizontal_lines, 0)
    
    def draw_lines_animated(self, lines, index):
        """가로선을 애니메이션으로 그리기"""
        if index >= len(lines):
            # 모든 선이 그려지면 결과 계산
            self.window.after(500, self.calculate_result)
            return
        
        x1, y, x2, y2, connection = lines[index]
        
        # 가로선 그리기
        self.canvas.create_line(
            x1, y, x2, y2,
            fill='#e74c3c',
            width=4,
            tags="horizontal_line"
        )
        
        # 연결점 표시
        self.canvas.create_oval(
            x1-3, y-3, x1+3, y+3,
            fill='#c0392b',
            outline='#c0392b',
            tags="horizontal_line"
        )
        self.canvas.create_oval(
            x2-3, y2-3, x2+3, y2+3,
            fill='#c0392b',
            outline='#c0392b',
            tags="horizontal_line"
        )
        
        # 다음 선 그리기
        self.window.after(100, lambda: self.draw_lines_animated(lines, index + 1))
    
    def calculate_result(self):
        """편가르기 결과 계산"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        people_count = len(self.people)
        
        margin = 80
        ladder_width = canvas_width - 2 * margin
        
        if people_count > 1:
            line_spacing = ladder_width / (people_count - 1)
        else:
            line_spacing = ladder_width
        
        # 각 사람의 경로 추적
        final_positions = list(range(people_count))
        
        # 가로선 정보 수집
        horizontal_connections = []
        for item in self.canvas.find_withtag("horizontal_line"):
            coords = self.canvas.coords(item)
            if len(coords) == 4:  # 선인 경우
                x1, y1, x2, y2 = coords
                # 어느 세로선들을 연결하는지 계산
                pos1 = round((x1 - margin) / line_spacing)
                pos2 = round((x2 - margin) / line_spacing)
                if 0 <= pos1 < people_count and 0 <= pos2 < people_count:
                    horizontal_connections.append((y1, pos1, pos2))
        
        # y좌표 기준으로 정렬
        horizontal_connections.sort()
        
        # 경로 추적
        for y, pos1, pos2 in horizontal_connections:
            # pos1과 pos2 위치의 사람들을 교환
            idx1 = final_positions.index(pos1)
            idx2 = final_positions.index(pos2)
            final_positions[idx1], final_positions[idx2] = final_positions[idx2], final_positions[idx1]
        
        # 팀 재편성
        new_teams = [[] for _ in range(len(self.teams))]
        team_sizes = [len(team) for team in self.teams]
        
        person_idx = 0
        for team_idx, size in enumerate(team_sizes):
            for _ in range(size):
                if person_idx < len(final_positions):
                    original_person_idx = final_positions[person_idx]
                    new_teams[team_idx].append(self.people[original_person_idx])
                    person_idx += 1
        
        # 결과 표시
        self.show_result(new_teams)
        self.animation_running = False
    
    def show_result(self, new_teams):
        """결과 표시"""
        # 기존 결과 제거
        self.canvas.delete("result")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 결과 배경
        result_y = canvas_height - 120
        self.canvas.create_rectangle(
            20, result_y - 10, canvas_width - 20, canvas_height - 20,
            fill='#ecf0f1',
            outline='#bdc3c7',
            width=2,
            tags="result"
        )
        
        # 결과 제목
        self.canvas.create_text(
            canvas_width // 2, result_y + 10,
            text="🎉 편가르기 결과 🎉",
            font=('맑은 고딕', 16, 'bold'),
            fill='#2c3e50',
            tags="result"
        )
        
        # 팀별 결과
        team_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        
        for i, team in enumerate(new_teams):
            if team:  # 팀에 멤버가 있는 경우만
                color = team_colors[i % len(team_colors)]
                team_text = f"팀 {i+1}: {', '.join(team)}"
                
                self.canvas.create_text(
                    canvas_width // 2, result_y + 35 + i * 20,
                    text=team_text,
                    font=('맑은 고딕', 12, 'bold'),
                    fill=color,
                    tags="result"
                )
    
    def reset_game(self):
        """게임 리셋"""
        self.game_frame.destroy()
        self.teams = []
        self.people = []
        self.ladder_lines = []
        self.canvas = None
        self.animation_running = False
        self.create_setup_frame()
    
    def run(self):
        """게임 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    game = LadderGame()
    game.run()
