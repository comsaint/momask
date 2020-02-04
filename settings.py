import time
from pathlib import Path

CUR_TIMESTAMP = str(int(time.time()))

# Folder paths
ROOT_FOLDER = Path(__file__).parent.absolute()
DATA_FOLDER = ROOT_FOLDER / 'data'
