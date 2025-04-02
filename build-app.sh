#!/bin/bash

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