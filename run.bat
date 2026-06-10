@echo off
REM Creates venv, installs requirements and runs generator
if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python generate_cards_html.py
pause
