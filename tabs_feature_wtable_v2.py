import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import pymysql as mysql

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
], style={'background':'rgba(0,146,184,0.4)'})

conn =  mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
query = "SELECT * FROM elektrana WHERE Vrijeme >= '2019-02-04 07:00:00' AND Vrijeme <= '2019-02-04 17:00:00'"
df = pd.read_sql(query, conn)

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
                                  name='Snaga AC'
                                    )
                          ],
                    layout=go.Layout(
                        title='test plot with pandas',
                        showlegend=True,
                        yaxis=dict(title='Snaga u W'),
                        xaxis=dict(title='Vrijeme'),
                                    )
                                ),
                style={'height': 500},
                id='my-graph'
                     ),
            html.Div([
            html.H3('Live podaci (5-minutni korak):'),
            html.P("Vrijeme: {}".format(df.iloc[-1,0])),
            html.P("Snaga AC: {}W".format(df.iloc[-1,2])),
            html.P("Snaga DC: {}W".format(df.iloc[-1,1])),
            html.P("Učinkovitost: {}%".format(df.iloc[-1,3])),
            html.P("Max. snaga danas: {}W".format(df.iloc[-1,4])),
            html.P("Frekvencija mreže: {}Hz".format(df.iloc[-1,5])),
            html.P("Temp. konverzije: {}°C".format(df.iloc[-1,6])),
            html.P("Energije danas: {}kW".format(df.iloc[-1,7])),
            html.P("Energije u tjednu: {}kW".format(df.iloc[-1,8])),
            html.P("Energije u mjesecu: {}kW".format(df.iloc[-1,9])),
            html.P("Energije u godini: {}kW".format(df.iloc[-1,10])),
            html.P("Energije ukupno: {}kW".format(df.iloc[-1,11])),
                     ], style={'marginBottom': 50, 'marginTop': 25, 'text-align': 'center'}
                    )
                    ])
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