import time
from pathlib import Path

CUR_TIMESTAMP = str(int(time.time()))

# Folder paths
ROOT_FOLDER = Path.cwd()
DATA_FOLDER = ROOT_FOLDER / 'data'
