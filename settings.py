import time
from pathlib import Path

# globals
UPLOAD_TO_CLOUD = True
CUR_TIMESTAMP = str(int(time.time()))
LIST_MODES = ['phq', 'hc', 'org']

# Local folder paths
ROOT_FOLDER = Path(__file__).parent.absolute()
DATA_FOLDER = ROOT_FOLDER / 'data'

# Cloud
GCP_PROJECT = 'beaming-crowbar-94213'
CLOUD_STORAGE_BUCKET = 'gs://momask'

