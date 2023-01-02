import dash_bootstrap_components as dbc
from dash import html, Dash,dcc
import pandas as pd
import plotly.express as px

app = Dash(name=__name__,external_stylesheets=[dbc.themes.LUX])

PLOTLY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Ukraine.svg/1200px-Flag_of_Ukraine.svg.png"

def spacer():
    return html.Div(html.Br())

search_bar = dbc.Row(
    [
        html.Div([
                    dcc.Dropdown(['News based sizing', 'Population based sizing', 'View vehicle movement'], 'Select one mode: ', id='mode-dropdown'),
                    #html.Div(id='dd-output-container')
                ]),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Ukraine Conflict Mapper", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    )
)

mapper = dbc.Container(children=[
    dbc.Row(children=[
        dbc.Col(width={"size":4,"order":'first'},children=[
            html.Div(children=[
                html.H2('Settings',style={'text-align': 'center','padding-bottom':'.em'}),
                html.P(style={'textAlign':'justify'}, children=['This tool aims to help contextualize and visualize the ongoing conflict in Ukraine.']),
                html.H5('Select mapping mode: '),
                html.Div([
                    dcc.Dropdown(['News based sizing', 'Population based sizing', 'View vehicle movement'], 'Select one mode: ', id='mode-dropdown'),
                    html.Div(id='dd-output-container')
                ]),
                spacer(),
                html.Button('Change Mode',className='btn btn-primary')
            ])           
        ]),
        dbc.Col(width={"size":True,"order":'last'},children=[
            html.Div(children=[
                html.H2('Map',style={'text-align': 'center','padding-bottom':'.4em'}),
                html.Iframe(id='map',srcDoc=open('Mapas/archivos mapas/index.html','r').read(),width='100%',height='480')
            ])
        ]),
    ],justify="evenly"),
    dbc.Row([
        dbc.Col([
            html.H1('Hi')
        ])
    ])
])



footer=dbc.Container(children=[
    spacer(),
    html.H1('Footer')
])

app.layout = dbc.Container(children=[
    navbar,
    spacer(),
    mapper,
    footer,

],)

if __name__=="__main__":
    app.run_server(debug=True)