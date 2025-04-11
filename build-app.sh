#!/bin/bash
pip install venv

python3 -m venv venv

source venv/bin/activate

#install required packages
./scripts/install-dependencies.sh

#install python packages
pip install -r requirements.txt

#build the app
pyinstaller --onefile --add-binary "/usr/bin/lftp:." --icon "./ico/esp.ico" app.py

# deactivate the virtual environment
deactivate

#remove venv and build files.
rm -rf build
rm -rf venv


