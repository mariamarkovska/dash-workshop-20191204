# Dash web app to visualize Spotify data from 2017-2018
# Version 2019-11-22
# Author: Maria Markovska

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd
import plotly.graph_objs as go
from datetime import datetime


## Read data from file
df = pd.read_csv("spotifys-worldwide-daily-song-ranking/data.csv")

# Filter on country-code 'se' for Sweden
df = df[df.Region == 'se']

# Define the dash app
app = dash.Dash()

# App layout
app.layout = html.Div(children=[

    html.H1(children='Spotify Swedish Top 10 (2017-2018)'),

    html.Label('Choose a day:'),

    dcc.DatePickerSingle(
        id='input-day-picker',
        min_date_allowed=datetime(2017, 1, 1),
        max_date_allowed=datetime(2018, 1, 1),
        initial_visible_month=datetime(2017, 1, 1),
        date=datetime.strftime(datetime(2017, 1, 1), '%Y-%m-%d')
    ),

    dash_table.DataTable(
        id = 'top-10-table',
        columns = [{"name": i, "id": i,} for i in (df.columns)]
    ),

    dcc.Graph(
        id = 'graph-streams-over-time'
    ),
])


# App functionality (callbacks)

# Update displayed table when a day is chosen
@app.callback(
    Output('top-10-table','data'),
    [Input('input-day-picker','date') ]
)

def filter_on_date(input_date):
    # Filter dataframe on chosen date
    filtered_df = df[df.Date == input_date]

    # Choose top 10 for display
    top_10_df = filtered_df[filtered_df.Position <= 10]

    # Convert to dictionary format (data format of a dash DataTable)
    data = top_10_df.to_dict('rows')

    # Return result to the displaying table
    return data



# Update graph when a day is chosen
@app.callback(
    Output('graph-streams-over-time','figure'),
    [Input('input-day-picker','date') ]
)

def update_graph(input_date):
    # Filter dataframe on chosen date
    filtered_df = df[df.Date == input_date]

    # Choose top 1 for graph
    top_1_df = filtered_df[filtered_df.Position <= 1]

    # Get URL, Track Name and Artist from top 1
    top_1_URL = top_1_df.URL.to_numpy()[0]
    top_1_track_name = top_1_df["Track Name"].to_numpy()[0]
    top_1_artist = top_1_df["Artist"].to_numpy()[0]

    # Find the top 1 URL in the global dataframe to get streams over time
    all_time_streams = df[df.URL == top_1_URL]    

    # Return results in format defined for a dcc.Graph figure
    return {
        'data': [
            {'x': all_time_streams.Date, 'y': all_time_streams.Streams, 'type': 'line'}
        ],
        'layout': {
            'title' : go.layout.Title(
                text=f"Streams over time: {top_1_track_name} - {top_1_artist}",
                font=dict(size=24, color="#000000")
            )
        }
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)