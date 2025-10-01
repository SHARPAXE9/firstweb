# Python GUI 애플리케이션 모음

이 프로젝트는 Python tkinter를 사용한 다양한 GUI 애플리케이션과 Windows 실행파일(.exe) 생성 방법을 포함합니다.

## 📁 프로젝트 구성

### 애플리케이션
- **`ladder_game.py`** - 편가르기 사다리 게임
  - 2-6개 팀 설정 가능
  - 각 팀당 최대 4명까지 인원 입력
  - 랜덤 이름 생성 기능
  - 애니메이션 사다리 그리기
  - 실시간 편가르기 결과 표시

- **`calculator.py`** - 계산기 애플리케이션
  - 기본 사칙연산 기능
  - GUI 기반 계산기

- **`hello_app.py`** - 간단한 인사 애플리케이션
  - tkinter GUI 기본 예제

### 빌드 도구
- **`build_exe.bat`** - 실행파일 자동 생성 스크립트
- **`requirements.txt`** - 필요한 패키지 목록
- **`python_setup_guide.md`** - Python 설치 및 실행파일 생성 가이드

## 🚀 실행 방법

### Python으로 직접 실행
```bash
# 사다리 게임 실행
python ladder_game.py

# 계산기 실행
python calculator.py

# Hello 앱 실행
python hello_app.py
```

### 실행파일(.exe) 생성

#### 자동 빌드 (권장)
```bash
build_exe.bat
```

#### 수동 빌드
```bash
# PyInstaller 설치
pip install pyinstaller

# 실행파일 생성 예시
pyinstaller --onefile --windowed --name="LadderGame" ladder_game.py
pyinstaller --onefile --windowed --name="Calculator" calculator.py
pyinstaller --onefile --windowed --name="HelloApp" hello_app.py
```

## 📋 PyInstaller 옵션 설명

- `--onefile`: 모든 의존성을 포함한 단일 실행파일 생성
- `--windowed`: 콘솔 창 숨기기 (GUI 앱용)
- `--name="AppName"`: 생성될 실행파일 이름 지정
- `--icon=icon.ico`: 아이콘 파일 지정 (선택사항)

## 📦 생성된 파일

실행파일은 `dist/` 폴더에 생성됩니다.

## ⚠️ 주의사항

- 첫 실행 시 바이러스 백신 프로그램에서 경고가 나올 수 있습니다.
- 실행파일 크기가 클 수 있습니다 (Python 런타임 포함).
- 다른 컴퓨터에서 실행하려면 해당 OS와 호환되는 환경에서 빌드해야 합니다.

## 🛠️ 개발 환경

- Python 3.x
- tkinter (Python 기본 포함)
- PyInstaller (실행파일 생성용)

## 📝 라이선스

MIT License
