@echo off
@chcp 65001 1> NUL 2> NUL

cd /D "%~DP0"

if exist venv\ (
  echo 이미 셋팅되어 있어요.
) else (
  python -m venv venv
  call venv\scripts\activate

  pip install -r requirements.txt

  echo 셋팅이 완료되었습니다.
)
TIMEOUT /T 10