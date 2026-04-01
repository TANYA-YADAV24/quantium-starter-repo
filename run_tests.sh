#!/bin/bash
set -e
export PATH="/c/Users/hp/.wdm/drivers/chromedriver/win64/146.0.7680.165/chromedriver-win32:$PATH"

echo '--- Activating virtual environment ---'
source venv/Scripts/activate

echo '--- Running test suite ---'
python -m pytest test_app.py -v