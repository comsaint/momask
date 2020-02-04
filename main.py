from scraper import run_scraper
from rparser import run_parser
from processing import run_processor
from settings import DATA_FOLDER

# create data folder
DATA_FOLDER.mkdir(exist_ok=True)

p_phq, p_hc, p_org = run_scraper()
f_parsed = run_parser(path_to_phq=p_phq, path_to_hc=p_hc, path_to_org=p_org)
run_processor()
