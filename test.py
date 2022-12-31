import dash_bootstrap_components as dbc
from dash import html, Dash,dcc
import pandas as pd
import plotly.express as px

app = Dash(name=__name__,external_stylesheets=[dbc.themes.LUX])

PLOTLY_LOGO = "logo.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",   
        ),
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
                        dbc.Col(dbc.NavbarBrand("Ukranian Conflict Mapper", class_name="ms-2")),
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
        ],),
)

row = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(width={"size":4,"order":'first'},children=[html.Div(children=[
                    html.H1(children=['Settings']),
                    html.P(children=['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras eleifend tincidunt ornare. Nam at egestas neque, nec hendrerit felis. Maecenas vehicula, sem nec tincidunt luctus, lectus turpis viverra massa, ut venenatis risus risus in odio. Maecenas sit amet eros in mi blandit ullamcorper dapibus nec eros. Nam varius purus venenatis, euismod metus in, pellentesque leo. Nulla facilisi. Aliquam luctus ex non orci rhoncus tristique. Sed rhoncus velit dolor, vel aliquam ipsum malesuada eu. Pellentesque rutrum lacus vel mauris egestas accumsan. Aenean lobortis nec mauris non hendrerit.'],style={'textAlign':'justify'}),
                    html.Div(children=[
                        html.P(children=['Select mapping mode: ']),
                        dbc.DropdownMenu(
                            label="Select one mode: ",
                            children=[
                                dbc.DropdownMenuItem("News based sizing"),
                                dbc.DropdownMenuItem("Population based sizing"),])
                    ]),
                    
                ])]),
                dbc.Col(class_name='btn btn-warning disabled', width={"size":True,"order":'last'},children=[html.Div(children=[

                ])]),
            ],

        ),
    ]
)

footer=dbc.Container(children=[
    html.Div(html.Br()),
    html.H1('Footer')
])

app.layout = dbc.Container(children=[
    navbar,
    html.Div(html.Br()),
    row,
    footer,

],)

if __name__=="__main__":
    app.run_server(debug=True)