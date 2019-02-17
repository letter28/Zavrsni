import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.H1('Fotonaponska elektrana FN1-Riteh: Podaci o proizvodnji'),
    dcc.Tabs(id="my-tabs", value='tab-1-example', children=[
        dcc.Tab(label='Graficki prikaz trenutacne proizvodnje', value='tab-1'),
        dcc.Tab(label='Tablica s podacima o proizvodnji', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

df = pd.DataFrame(data=[['7:00', 100, 90],['8:00', 200, 190],['9:00', 300, 280],['10:00', 480, 460],
                        ['11:00', 750, 720],['12:00', 1190, 1140],['13:00', 1700, 1640],['14:00', 2100, 2020],
                        ['15:00', 2300, 2220],['16:00', 2050, 1990],['17:00', 1620, 1570],['18:00', 890, 840],
                        ['19:00', 450, 430],['20:00', 40, 30]], columns=['Vrijeme', 'Snaga_AC', 'Snaga_DC'])

@app.callback(Output('tabs-content', 'children'),
              [Input('my-tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Testni prikaz simulirane proizvodnje'),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                          go.Scatter(
                                  x=df['Vrijeme'],
                                  y=df['Snaga_DC'],
                                  name='Snaga DC',
                                  ),
                          go.Scatter(
                                  x=df['Vrijeme'],
                                  y=df['Snaga_AC'],
                                  name='Snaga AC',
                                  )
                              ],
                    layout=go.Layout(
                        title='test plot with pandas',
                        showlegend=True,
                        yaxis=dict(title='Snaga u W'),
                        xaxis=dict(title='Vrijeme')
                                    )
                                ),
                style={'height': 300},
                id='my-graph'
                     )
                   ]
                )
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Podaci o prethodnoj proizvodnji'),
            dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
)
                        ])

if __name__ == '__main__':
    app.run_server(debug=True)