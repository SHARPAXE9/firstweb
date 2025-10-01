@echo off
echo PyInstaller를 사용하여 실행파일을 생성합니다...
echo.

REM PyInstaller 설치
echo [1/3] PyInstaller 설치 중...
pip install pyinstaller

echo.
echo [2/3] 실행파일 생성 중...
REM 단일 파일로 실행파일 생성 (--onefile)
REM 콘솔 창 숨기기 (--windowed)
REM 아이콘 추가 가능 (--icon=icon.ico)
pyinstaller --onefile --windowed --name="HelloApp" hello_app.py

echo.
echo [3/3] 완료!
echo 생성된 실행파일 위치: dist\HelloApp.exe
echo.
pause
