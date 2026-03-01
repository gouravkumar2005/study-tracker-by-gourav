@echo off
echo Setting up Python 3.11 environment for OpenCV...

REM Download Python 3.11.9 installer
echo Downloading Python 3.11.9...
curl -o python-3.11.9-amd64.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

REM Install Python 3.11.9 (silent install, add to PATH)
echo Installing Python 3.11.9...
python-3.11.9-amd64.exe /quiet InstallAllUsers=0 PrependPath=1

REM Wait for installation
timeout /t 10 /nobreak

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv311

REM Activate virtual environment and install requirements
echo Activating virtual environment and installing packages...
call venv311\Scripts\activate.bat
pip install --upgrade pip
pip install opencv-python==4.8.1.78 Pillow==10.0.1

echo Setup complete! Use 'venv311\Scripts\activate.bat' to activate the environment.
pause
