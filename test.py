import dash_bootstrap_components as dbc
from dash import html, Dash,dcc
import pandas as pd
import plotly.express as px

app = Dash(name=__name__,external_stylesheets=[dbc.themes.LUX])

PLOTLY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Ukraine.svg/1200px-Flag_of_Ukraine.svg.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                        dbc.Col([
                                    html.Img(src=PLOTLY_LOGO, height="50px")
                                ],width={"size":2,"order":'first'}),
                        dbc.Col([
                                    html.H1("Ukranian Conflict Mapper")
                                ],width={"size":True,"order":'last'})
                            
                        
                    ]),
        ])
)

mapper = html.Div(children=[
    dbc.Row(children=[
        dbc.Col(width={"size":4,"order":'first'},children=[
            html.Div(children=[
                html.H2('Settings',style={'text-align': 'center'}),
                html.P(style={'textAlign':'justify'}, children=['This tool aims to help contextualize and visualize the ongoing conflict in Ukraine.']),
                html.H5('Select mapping mode: '),
                html.Div([
                    dcc.Dropdown(['News based sizing', 'Population based sizing', 'View vehicle movement'], 'Select one mode: ', id='mode-dropdown'),
                    html.Div(id='dd-output-container')
                ])
            ])           
        ]),
        dbc.Col(width={"size":True,"order":'last'},children=[
            html.Div(children=[
                html.H2('Map',style={'text-align': 'center'}),
                html.Iframe(id='map',srcDoc=open('Mapas/archivos mapas/index.html','r').read(),width='100%',height='480')
            ])
        ]),
    ],justify="evenly")
])

footer=dbc.Container(children=[
    html.Div(html.Br()),
    html.H1('Footer')
])

app.layout = dbc.Container(children=[
    navbar,
    html.Div(html.Br()),
    mapper,
    footer,

],)

if __name__=="__main__":
    app.run_server(debug=True)