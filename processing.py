"""
script for post-processing the parsed file `parsed_xxxxxx.csv`.
"""
from settings import DATA_FOLDER
import pandas as pd


def read_parsed_file(path=None):
    if path is None:  # read and concat all parsed (default)
        p = DATA_FOLDER.glob('parsed_*.csv')
        files = [x for x in p if x.is_file()]
        lst_df = []
        for f in files:
            df = pd.read_csv(f, encoding='utf-8')
            lst_df.append(df)
        dfs = pd.concat(lst_df)
    else:  # for debug, read only 1 file
        dfs = pd.read_csv(path, encoding='utf-8')
    return dfs


def process_data(df):
    # filter out unused fields, keep Chinese only for now
    usecols = ['code', 'name', 'address', 'officehour', 'tel', 'fax', 'nightpharmacy', 'maskstock', 'parsed_timestamp']
    df = df[usecols]
    # split the df into 2 tables, [1]info of pharmacy (name, address etc.) and [2]mask stock, with `code` as foreign key
    info = df[['code', 'name', 'address', 'tel', 'fax', 'nightpharmacy']].drop_duplicates().set_index('code')
    stock = df[['code', 'maskstock', 'parsed_timestamp']]
    # add a human readable timestamp
    stock['human_parsed_timestamp'] = pd.to_datetime(stock['parsed_timestamp'], unit='s') + pd.Timedelta('08:00:00')
    return info, stock


def write_output_file(df_info, df_stock):
    p_info, p_stock = DATA_FOLDER / 'info.csv', DATA_FOLDER / 'stock.csv'
    df_info.to_csv(p_info, encoding='utf-8')
    df_stock.to_csv(p_stock, encoding='utf-8', index=False)
    return 0


def run_processor():
    # read and concat all files
    df= read_parsed_file()
    info, stock = process_data(df)
    write_output_file(info, stock)
    print(info.head())
    print(stock.head())
    return 0
