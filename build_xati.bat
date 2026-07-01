@echo off
echo Building XATI Enterprise...

python -m PyInstaller --noconsole --onefile --name "XATI" --icon=assets/icon.ico --add-data "assets/icon.ico;assets" --add-data "assets/icon.png;assets" --exclude-module matplotlib --exclude-module scipy --exclude-module numpy --exclude-module pandas --exclude-module PyQt5 --exclude-module PyQt6 --exclude-module PySide6 --exclude-module IPython --exclude-module jupyter --version-file=version_info.txt src/main.py

echo Build complete! The executable is in the 'dist' folder.
pause
