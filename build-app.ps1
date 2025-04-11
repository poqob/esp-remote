# Windows PowerShell build script for ESP Remote

# Install venv
pip install venv

# Create virtual environment
python -m venv venv

# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Install Python packages
pip install -r requirements.txt

# Check if Chocolatey is installed
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey is not installed. Please install it from https://chocolatey.org/install" -ForegroundColor Red
    exit 1
}

# Install lftp
choco install -y lftp

# Build the app with PyInstaller
pyinstaller --onefile --add-binary "C:/Program Files (x86)/lftp/bin/lftp.exe;." --icon "./ico/esp.ico" app.py

# Deactivate virtual environment
deactivate

# Clean up build files
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "venv" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Build completed successfully!" -ForegroundColor Green