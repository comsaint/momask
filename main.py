from scraper import run_scraper
from rparser import run_parser
from processing import run_processor

p_phq, p_hc, p_org = run_scraper()
f_parsed = run_parser(path_to_phq=p_phq, path_to_hc=p_hc, path_to_org=p_org)
run_processor()
