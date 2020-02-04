import plotly.express as px
import pandas as pd
from settings import DATA_FOLDER

df = pd.read_csv(DATA_FOLDER / 'info_all_20200203.csv')
df['text'] = df['name'] + '<br>Address' + df['address']
df['size'] = 6

# TODO: load mask stock data

# plot viz
fig = px.scatter_mapbox(df, lat="y", lon="x",
                        hover_name="text",
                        #hover_data=["State", "Population"],
                        zoom=14,
                        size='size',
                        size_max=10,
                        color='poi_type',
                        opacity=1,
                        #height=800
                        )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":600,"t":50,"l":300,"b":0})
fig.show()
