from Python.libraries import *

from Python.RSS_puller_parser import main as main_rss
from Python.queries import main as main_queries
from Python.mapper import main as main_mapper

app = Dash(name=__name__,external_stylesheets=[dbc.themes.LUX])

PLOTLY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Ukraine.svg/1200px-Flag_of_Ukraine.svg.png"

def spacer():
    return html.Div(html.Br())

search_bar = dbc.Row(
    [
        html.Div([
            dbc.DropdownMenu(
                label="Select mapping mode: ",
                align_end=True,
                children=[
                    dbc.DropdownMenuItem("Infrastructure"),
                    dbc.DropdownMenuItem("News and Population"),
                    dbc.DropdownMenuItem("BTG movement mapper"),
            ])
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
                html.H2('Settings',style={'text-align': 'center','padding-bottom':'.1em'}),
                html.P(style={'textAlign':'justify'}, children=['This tool aims to help contextualize and visualize the ongoing conflict in Ukraine.']),
            ])           
        ]),
        dbc.Col(width={"size":True,"order":'last'},children=[
            html.Div(children=[
                html.H2('Map',style={'text-align': 'center','padding-bottom':'.4em'}),
                html.Iframe(id='map',srcDoc=open('./Assets/Maps/index.html','r').read(),width='100%',height='300')
            ])
        ]),
    ],justify="evenly")
])

news=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Recent News')
        ])
    ])
])

footer=dbc.Container(children=[
    
])

app.layout = dbc.Container(children=[
    navbar,
    mapper,
    news,
    footer,

],)

if __name__=="__main__":
    app.run_server(debug=True)