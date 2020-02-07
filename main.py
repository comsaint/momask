from scraper import run_scraper
from rparser import run_parser
from processing import run_processor
from viz_processing import viz_processing
from settings import DATA_FOLDER
from settings import UPLOAD_TO_CLOUD, CLOUD_STORAGE_BUCKET, LIST_MODES

# create data folder
DATA_FOLDER.mkdir(exist_ok=True)

p_phq, p_hc, p_org = run_scraper()
f_parsed = run_parser(path_to_phq=p_phq, path_to_hc=p_hc, path_to_org=p_org)
run_processor()
df = viz_processing()

# upload the stock data to cloud storage for app to access
if UPLOAD_TO_CLOUD is True:
    from commonfunc import upload_to_gcs
    from settings import GCP_PROJECT
    upload_to_gcs(project=GCP_PROJECT,
                  src_file=str((DATA_FOLDER / 'df.csv').resolve()),
                  dst_bucket=CLOUD_STORAGE_BUCKET,
                  dst_blob_name='df.csv'
                  )
