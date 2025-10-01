# Python 설치 및 실행파일 생성 가이드

## 1. Python 설치

### Windows에서 Python 설치하기:

1. **Python 공식 웹사이트 방문**
   - https://www.python.org/downloads/ 접속
   - "Download Python 3.x.x" 버튼 클릭

2. **설치 옵션**
   - ✅ "Add Python to PATH" 체크박스 **반드시 선택**
   - "Install Now" 클릭

3. **설치 확인**
   ```cmd
   python --version
   pip --version
   ```

## 2. 실행파일 생성 단계

### 방법 1: 배치 파일 사용 (간편)
```cmd
build_exe.bat
```

### 방법 2: 수동 명령어
```cmd
# 1. PyInstaller 설치
pip install pyinstaller

# 2. 실행파일 생성
pyinstaller --onefile --windowed --name="HelloApp" hello_app.py

# 3. 생성된 파일 확인
dir dist\
```

## 3. 실행파일 옵션

| 옵션 | 설명 |
|------|------|
| `--onefile` | 단일 실행파일 생성 |
| `--windowed` | 콘솔 창 숨기기 |
| `--name="이름"` | 실행파일 이름 지정 |
| `--icon=icon.ico` | 아이콘 설정 |
| `--add-data "src;dest"` | 추가 파일 포함 |

## 4. 문제 해결

### Python이 인식되지 않는 경우:
1. Python 재설치 시 "Add to PATH" 선택
2. 환경변수 수동 설정:
   - 시스템 속성 → 고급 → 환경 변수
   - Path에 Python 설치 경로 추가

### 실행파일이 큰 경우:
```cmd
# 필요한 모듈만 포함
pyinstaller --onefile --windowed --exclude-module matplotlib hello_app.py
```

### 바이러스 백신 오탐:
- Windows Defender 예외 처리 추가
- 디지털 서명 추가 고려
