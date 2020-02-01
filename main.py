from scraper import run_scraper
from rparser import run_parser
from processing import run_processor

p_phq, p_hc = run_scraper()
f_parsed = run_parser(path_to_phq=p_phq, path_to_hc=p_hc)
run_processor()
