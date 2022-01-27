# this might help me break the project up
# https://www.purfe.com/dash-project-structure-multi-tab-app-with-callbacks-in-different-files/

from server import app, server
from dash.development.base_component import Component
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
#from convert_time import convertTime
import callbacks

# stop pandas from issuing ceratain warnings
pd.options.mode.chained_assignment = None  # default='warn'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# set some colors
colors = {
    'background': '#111111',
    'text': '#00ABE1'
}

# ingest data
data = pd.read_csv('https://github.com/CBlumini/heroku_dep_2/raw/main/Santa-Cruz-Sprint.csv', header=0, index_col=None)
females = data[data['Gender'] == 'F']


def convertTime (time):
    temp = time.split(':')
    timeMinutes = (int(temp[0])*60)+int(temp[1])+int(temp[2])/60
    return timeMinutes

# the data does not come in the right form to do math on it. So convert the times to minutes and decimal seconds
# maybe setup a compute file to do this by itself later
def create_time_columns(bare_frame):

    # convert to integers
    bare_frame["Swim Minutes"] = bare_frame["Swim"].apply(convertTime)
    bare_frame["T1 Minutes"] = bare_frame["T1"].apply(convertTime)
    bare_frame["Bike Minutes"] = bare_frame["Bike"].apply(convertTime)
    bare_frame["T2 Minutes"] = bare_frame["T2"].apply(convertTime)
    bare_frame["Run Minutes"] = bare_frame["Run"].apply(convertTime)
    # bare_frame["Elapsed Minutes"] = bare_frame["Chip Elapsed"].apply(convert_time)

    # create cumulative times
    bare_frame["Swim+T1"] = round(bare_frame["Swim Minutes"] + bare_frame["T1 Minutes"], 2)
    bare_frame["Plus Bike"] = round(bare_frame["Swim+T1"] + bare_frame["Bike Minutes"], 2)
    bare_frame["Plus T2"] = round(bare_frame["Plus Bike"] + bare_frame["T2 Minutes"], 2)
    bare_frame["Total"] = round(bare_frame["Plus T2"] + bare_frame["Run Minutes"], 2)

    return bare_frame


time_df = create_time_columns(females)

reduced2 = time_df[["Name", "Swim Minutes", "Swim+T1", "Plus Bike", "Plus T2", "Total", "Gender Place"]]
reduced2["Start"] = 0
reduced2 = reduced2[reduced2['Total'] > 60]

# name the columns for the data table
dash_columns = ["Bib", "Name", "Age", "Gender", "City", "Swim", "T1", "Bike", "T2", "Run", "Chip Elapsed", "Div Place",
                "Age Place",
                "Gender Place"]

# layout the page
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Welcome to the Triathlon Data Analyzer'))
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='This app allows for performance plotting of certain local bay area triathlons.'))
        ]),                            
        dash_table.DataTable(
            id='table-sorting-filtering',
            columns=[{'name': i, 'id': i} for i in dash_columns],
            data=time_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_cell={
                'height': '90',
                # 'minWidth': '110%',
                'minWidth': '60px', 'width': '100px', 'maxWidth': '140px',
                'whiteSpace': 'normal', 'textAlign': 'center',
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'},
            style_cell_conditional=[{
                'if': {'column_id': 'Name'},
                'textAlign': 'center'
            }],
            page_current=0,
            page_size=15,
            filter_action='native',
            filter_query='',
            sort_action='native',
            sort_mode='single',
            sort_by=[],
            style_as_list_view=True,
            hidden_columns=[],
        ),

        dcc.Graph(
            id='graph-with-slider',
            # figure=scat
        ),

        dcc.Slider(
            id='scat-place-slider',
            min=reduced2['Gender Place'].min(),
            max=200,
            value=reduced2['Gender Place'].min(),
            # marks={str(year): str(year) for year in reduced2['Gender Place'].unique()},
            step=None,
            marks={
                10: '10',
                25: '25',
                50: '50',
                100: '100',
                200: '200'
            }
        ),

        dcc.Graph(
            id='par-with-slider',
            # figure=para_cor
        ),

        dcc.Slider(
            id='par-place-slider',
            min=reduced2['Gender Place'].min(),
            max=200,
            value=reduced2['Gender Place'].min(),
            # marks={str(year): str(year) for year in reduced2['Gender Place'].unique()},
            step=None,
            marks={
                10: '10',
                25: '25',
                50: '50',
                100: '100',
                200: '200'
            }
        ),
                      
    ])
])
        



