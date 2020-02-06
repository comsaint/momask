import plotly.express as px
import pandas as pd
from settings import DATA_FOLDER

df_info = pd.read_csv(DATA_FOLDER / 'info_all_20200203.csv', index_col='code')

# TODO: load mask stock data
df_stock_phq = pd.read_csv(DATA_FOLDER / 'stock_phq.csv', dtype={'code':str})
df_stock_hc = pd.read_csv(DATA_FOLDER / 'stock_hc.csv')
df_stock_org = pd.read_csv(DATA_FOLDER / 'stock_org.csv')

# rename some columns to be consistent
df_stock_hc.rename({'tolqty_diff': 'maskstock', 'licno': 'code'}, axis=1, inplace=True)
df_stock_org.rename({'tolqty_diff': 'maskstock', 'licno': 'code'}, axis=1, inplace=True)

# concat
df_stock = pd.concat([df_stock_phq, df_stock_hc, df_stock_org], axis=0)
usecols = ['code', 'maskstock', 'human_parsed_timestamp']
df_stock = df_stock[usecols]
df_stock.set_index('code', inplace=True)

# join
df = df_stock.join(df_info, how='left')

# most recent stock
df_recent = df.sort_values('human_parsed_timestamp', ascending=True).reset_index().drop_duplicates(subset='code', keep='last').sort_values('code', ascending=True)
df_recent['maskstock_str'] = df_recent['maskstock'].apply(str)

df_recent['text'] = df_recent['name'] + \
                  '<br>Address:<br>' + df_recent['address'] + \
                  '<br>Last updated time:' + df_recent['human_parsed_timestamp'] + \
                  '<br><b>Mask Stock: ' + df_recent['maskstock_str'] + '</b>'
df_recent['size'] = 10
df_recent.to_csv('df_recent.csv', index=False)

# plot viz
fig = px.scatter_mapbox(df_recent, lat="y", lon="x",
                        hover_name="text",
                        hover_data=['maskstock'],
                        zoom=13,
                        size='maskstock',
                        size_max=50,
                        color='poi_type',
                        opacity=0.9,
                        height=800
                        )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":500,"t":0,"l":0,"b":0})
fig.show()

