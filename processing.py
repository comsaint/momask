"""
script for post-processing the parsed file `parsed_xxxxxx.csv`.
"""
from settings import DATA_FOLDER
import pandas as pd


def read_parsed_file(mode, path=None):
    if path is None:  # read and concat all parsed (default)
        p = DATA_FOLDER.glob('parsed_{}_*.csv'.format(mode))
        files = [x for x in p if x.is_file()]
        lst_df = []
        for f in files:
            df = pd.read_csv(f, encoding='utf-8')
            lst_df.append(df)
        dfs = pd.concat(lst_df)
    else:  # for debug, read only 1 file
        dfs = pd.read_csv(path, encoding='utf-8')
    return dfs


def process_data(df, mode):
    if mode == 'phq':
        # filter out unused fields, keep Chinese only for now
        usecols = ['code', 'name', 'address', 'officehour', 'tel', 'fax', 'nightpharmacy', 'maskstock', 'parsed_timestamp']
        df = df[usecols]
        # split the df into 2 tables, [1]info of pharmacy (name, address etc.) and [2]mask stock, with `code` as foreign key
        info = df[['code', 'name', 'address', 'tel', 'fax', 'nightpharmacy']].drop_duplicates().set_index('code')
        stock = df[['code', 'maskstock', 'parsed_timestamp']]
    elif mode == 'hc':
        # filter out unused fields, keep Chinese only for now
        usecols = ['licno', 'name', 'tolqty_whs', 'tolqty_out', 'tolqty_diff', 'parsed_timestamp']
        df = df[usecols]
        # split the df into 2 tables, [1]info of health center (license and name) and [2]mask stock, with `licno` as foreign key
        info = df[['licno', 'name']].drop_duplicates().set_index('licno')
        stock = df[['licno', 'tolqty_whs', 'tolqty_out', 'tolqty_diff', 'parsed_timestamp']]
    elif mode == "org":
        # filter out unused fields, keep Chinese only for now
        usecols = ['licno', 'name', 'officehour', 'tel', 'parsed_timestamp', 'ispublic', 'istest', 'isstop',
                   'tolqty_whs', 'tolqty_out', 'tolqty_diff']
        df = df[usecols]
        # split the df into 2 tables, [1]info of health center (license and name) and [2]mask stock, with `licno` as foreign key
        info = df[['licno', 'name', 'officehour', 'tel', 'ispublic', 'istest', 'isstop']].drop_duplicates().set_index('licno')
        stock = df[['licno', 'tolqty_whs', 'tolqty_out', 'tolqty_diff', 'parsed_timestamp']]
    else:
        raise ValueError("Mode")
    # add a human readable timestamp
    stock['human_parsed_timestamp'] = pd.to_datetime(stock['parsed_timestamp'], unit='s') + pd.Timedelta('08:00:00')
    return info, stock


def write_output_file(df_info, df_stock, mode):
    p_info, p_stock = DATA_FOLDER / 'info_{}.csv'.format(mode), DATA_FOLDER / 'stock_{}.csv'.format(mode)
    df_info.to_csv(p_info, encoding='utf-8')
    df_stock.to_csv(p_stock, encoding='utf-8', index=False)
    return 0


def run_processor():
    # read and concat all files
    for mode in ['phq', 'hc', 'org']:
        df = read_parsed_file(mode=mode)
        info, stock = process_data(df, mode=mode)
        write_output_file(info, stock, mode=mode)
    return 0


if __name__ == "__main__":
    run_processor()
