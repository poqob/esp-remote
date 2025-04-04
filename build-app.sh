#!/bin/bash
pip install venv

python3 -m venv venv

# Check if the script is being run on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Running on Windows"
    # Activate the virtual environment
    source venv/Scripts/activate
else
    # Linux or macOS
    echo "Running on Linux or macOS"
    # Activate the virtual environment
    source venv/bin/activate
fi

#install required packages
./scripts/install-dependencies.sh

#install python packages
pip install -r requirements.txt

#build the app
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    pyinstaller --onefile --add-binary "C:/Program Files (x86)/lftp/bin/lftp.exe;." --icon "./ico/esp.ico" app.py
else
    pyinstaller --onefile --add-binary "/usr/bin/lftp:." --icon "./ico/esp.ico" app.py
fi

# deactivate the virtual environment
deactivate

#remove venv and build files.
rm -rf build
rm -rf venv


