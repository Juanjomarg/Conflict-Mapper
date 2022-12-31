import dash
from dash.dependencies import Input, Output
from dash import dcc, html

app = dash.Dash('example')


dcc.RadioItems(
                id='show-table',
                options=[{'label': i, 'value': i} for i in ['None', 'All', 'Alerts']],
                value='None',
                labelStyle={'display': 'inline-block'}
            )
html.Div([
        dash.dash_table.DataTable(
        id = 'datatable',
        data=today_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in today_df.columns],
        fixed_columns={ 'headers': True, 'data': 1 },
        fixed_rows={ 'headers': True, 'data': 0 },
        style_cell={
        # all three widths are needed
        'minWidth': '150px', 'width': '150px', 'maxWidth': '500px',
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        },
        style_table={'maxWidth': '1800px'},
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_deletable=True),
    ], style={'width': '100%'}, id='datatable-container')

@app.callback(
    dash.dependencies.Output('datatable-container', 'style'),
    [dash.dependencies.Input('show-table', 'value')])
def toggle_container(toggle_value):
    print(toggle_value, flush=True)
    if toggle_value == 'All':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)