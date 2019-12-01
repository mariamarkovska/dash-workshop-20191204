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

# Define the dash app & stylesheet (see CSS styleguide link on git)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# App layout (the looks)

app.layout = html.Div(children=[

	# Headers (1 and 4 means different sizes)
    html.H1(children='Spotify Swedish Top 10 year 2017'),
    html.H4('Choose a day'),

    # A date-picker component to use as a date input
    dcc.DatePickerSingle(
        id='input-day-picker',
        min_date_allowed=datetime(2017, 1, 1),
        max_date_allowed=datetime(2018, 1, 1),
        initial_visible_month=datetime(2017, 1, 1),
        date=datetime.strftime(datetime(2017, 1, 1), '%Y-%m-%d')
    ),

    # Table showing all columns in dataframe
    dash_table.DataTable(
        id = 'top-10-table',
        columns = [{"name": i, "id": i,} for i in (df.columns)]
    ),

    # A new row Div to put the two graphs next to each other
    html.Div([
        html.Div([
            dcc.Graph(id='bar-graph')
        ], className="six columns"), # six columns -> divide 50/50

        html.Div([
            dcc.Graph(id='pie-graph')
        ], className="six columns"),
    ], className="row"),

])


# App callbacks (the functionality)

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

# Update pie-graph when a day is chosen
@app.callback(
    Output('pie-graph','figure'),
    [Input('input-day-picker','date') ]
)

def update_pie_graph(input_date):
    # Filter dataframe on chosen date
    filtered_df = df[df.Date == input_date]

    # Choose top 10 for display
    top_10_df = filtered_df[filtered_df.Position <= 10]

    # Get top 10 songs
    songs = top_10_df["Track Name"].to_numpy()

    # Go through all data and calculate total steams for top 10 songs
    total_streams_list = []
    for song in songs:
        song_df = df[df["Track Name"] == song]
        total_streams = song_df["Streams"].sum()
        total_streams_list.append(total_streams)
    
    # Return a dcc.Graph figure containing a bar-chart
    return {
        'data': [
            go.Pie(values=total_streams_list, labels=songs)
        ],
        'layout': {
            'title' : go.layout.Title(
                text=f"Top 10 Songs: total streams 2017",
                font=dict(size=24, color="#000000")
            ),
            'showlegend' : False
        }
    }


# Update bar-graph when a day is chosen
@app.callback(
    Output('bar-graph','figure'),
    [Input('input-day-picker','date') ]
)

def update_line_graph(input_date):
    # Filter dataframe on chosen date
    filtered_df = df[df.Date == input_date]

    # Choose top 10 for display
    top_10_df = filtered_df[filtered_df.Position <= 10]

    # Get top 10 artists
    artists = top_10_df["Artist"].to_numpy()

    # Go through all data and calculate total steams for top 10 artists
    total_streams_list = []
    for artist in artists:
        artist_df = df[df["Artist"] == artist]
        total_streams = artist_df["Streams"].sum()
        total_streams_list.append(total_streams)
    
    # Return a dcc.Graph figure containing a bar-chart
    return {
        'data': [
            go.Bar(x=artists, y=total_streams_list)
        ],
        'layout': {
            'title' : go.layout.Title(
                text=f"Top 10 Artists: total streams 2017",
                font=dict(size=24, color="#000000")
            )
        }
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)