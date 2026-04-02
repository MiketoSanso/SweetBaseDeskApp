@echo off
cd %~dp0\..\..

echo Creating virtual environment...
python -m venv tech\venv

echo Installing dependencies...
call tech\venv\Scripts\activate && pip install -r tech\.config\requirements.txt

echo Running migrations...
call tech\venv\Scripts\activate && alembic -c tech\.config\alembic.ini upgrade head

echo Installing pre-commit hooks...
call tech\venv\Scripts\activate && pre-commit install --config tech\.config\.pre-commit-config.yaml

echo Setup complete!
pause