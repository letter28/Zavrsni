import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.H1('Fotonaponska elektrana FN1-Riteh: Podaci o proizvodnji'),
    dcc.Tabs(id="my-tabs", value='tab-1-example', children=[
        dcc.Tab(label='Graficki prikaz trenutacne proizvodnje 1', value='tab-1'),
        dcc.Tab(label='Tablica s podacima o proizvodnji', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('my-tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Graficki prikaz trenutacne proizvodnje'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'line',
                        'name': 'Snaga AC [W]'
                    }]
                }
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Podaci o prethodnoj proizvodnji')
                        ])


if __name__ == '__main__':
    app.run_server(debug=True)