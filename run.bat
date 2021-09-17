cd /D "%~DP0"

call venv\scripts\activate

set FLASK_APP=app.py
set FLASK_DEBUG=1
python -m flask run -p 15000