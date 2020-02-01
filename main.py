from scraper import run_scraper
from rparser import run_parser
from processing import run_processor

f_scraped = run_scraper()
f_parsed = run_parser(path_to_input=f_scraped)
run_processor()
