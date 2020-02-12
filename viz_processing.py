"""
Module to compile the data required for visualization.
"""
# Data processing
import pandas as pd
from settings import DATA_FOLDER, LIST_MODES


def viz_processing():
    # downlaod data from csv
    data_set = [pd.read_csv(DATA_FOLDER / 'stock_{}.csv'.format(mode)) for mode in LIST_MODES]

    # select the latest data
    stock = []
    for data in data_set:
        ff = data.parsed_timestamp == data.parsed_timestamp.max()
        stock.append(data[ff])

    # Record the latest time
    latest_time = str(data[ff].human_parsed_timestamp.unique()[0])

    # merge dataframes
    stock[0].rename(columns={'code': 'licno'}, inplace=True)
    phq = stock[0].copy()
    del phq['parsed_timestamp']
    hc = pd.concat([stock[1].licno, stock[1].tolqty_diff, stock[1].human_parsed_timestamp], axis=1)
    org = pd.concat([stock[2].licno, stock[2].tolqty_diff, stock[2].human_parsed_timestamp], axis=1)
    phq.columns = org.columns
    qty = pd.concat([phq, hc, org], axis=0, sort=False).reset_index(drop=True)

    # join tables with the coordinate data
    info = pd.read_csv(DATA_FOLDER / "map_info.csv", encoding='utf8')
    df = pd.concat([info, qty], axis=1)
    df['unit'] = '個'
    df = df.fillna(0)  # gov website removed some institutes without any announcement
    df['hov_txt'] = df['txt'] + df['tolqty_diff'].astype(int).astype(str) + df['unit']
    return df


def create_full_dataframe():
    # read stock
    lst_stocks = []
    mapping = {'maskstock': 'tolqty_diff', 'licno': 'code'}
    for mode in LIST_MODES:
        __df = pd.read_csv(DATA_FOLDER / 'stock_{}.csv'.format(mode))
        # rename columns to match
        __df.rename(mapping, axis=1, inplace=True)
        __df = __df.astype({'code': str})
        lst_stocks.append(__df)
    stock = pd.concat(lst_stocks)
    # read info
    info = pd.read_csv(DATA_FOLDER / 'info_all_20200203.csv')
    # join
    df_full = stock.merge(info, how='left', left_on='code', right_on='code')
    return df_full


def write_to_local(df, path):
    df.to_csv(path, index=False, encoding='utf-8')
    return 0


def run_viz_processing():
    df = viz_processing()
    df_full = create_full_dataframe()
    write_to_local(df, path=DATA_FOLDER / 'df.csv')
    write_to_local(df_full, path=DATA_FOLDER / 'df_full.csv')


if __name__ == "__main__":
    run_viz_processing()
