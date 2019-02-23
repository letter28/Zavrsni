import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
import pandas as pd
import pymysql as mysql
import time
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
                      html.H1('Fotonaponska elektrana FN1-Riteh: Podaci o proizvodnji', 
                              style={'color': 'rgb(255,255,255)',
                                     'text-align': 'center',
                                     'text-shadow':'1px 1px #000000'}),
                      html.Div(id='live-update-text'),
                      dcc.Graph(id='live-update-graph'),
                      dcc.Tabs(id="my-tabs", value='tab-1-example', children=[
                                                                              dcc.Tab(label='Grafički prikaz prethodne proizvodnje', value='tab-1'),
                                                                              dcc.Tab(label='Tablica s podacima o proizvodnji (u doradi)', value='tab-2')
                                                                             ]),
                      dcc.DatePickerRange(
                                          id='my-date-picker-range',
                                          min_date_allowed=dt(2019, 1, 1),
                                          max_date_allowed=dt.now(),
                                          initial_visible_month=dt(2019, 1, 2),
                                          start_date='',
                                          end_date=''
                                         ),
                      html.Div(id='tabs-content'),
                      dcc.Interval(id='my-interval', 
                                   interval=300*1000, 
                                   n_intervals=0)
                      ], style={'background':'rgb(0,146,184)'})

@app.callback(Output('live-update-text', 'children'),
              [Input('my-interval', 'n_intervals')])
def update_text(n):
    t1 = time.time()
    conn =  mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
    query = "SELECT * FROM elektrana"
    df = pd.read_sql(query, conn)
    style={'color':'rgb(255,255,255)', 'text-align':'center'}
    t2 = time.time()
    print('Vremena za update teksta: {}'.format(t2-t1))
    return html.Div([html.H3('Live podaci - 5-minutni korak:', style=style),
                    html.Div([
                             html.Div([
                                      html.H6("Vrijeme: {}".format(df.iloc[-1,0]), style=style),
                                      html.H6("Snaga AC: {}W".format(df.iloc[-1,2]), style=style),
                                      html.H6("Snaga DC: {}W".format(df.iloc[-1,1]), style=style),
                                      html.H6("Učinkovitost: {}%".format(df.iloc[-1,3]), style=style),
                                      html.H6("Max. snaga danas: {}W".format(df.iloc[-1,4]), style=style),
                                      html.H6("Frekvencija mreže: {}Hz".format(df.iloc[-1,5]), style=style),
                                      html.H6("Temp. konverzije: {}°C".format(df.iloc[-1,6]), style=style)],className='six columns'),
                             html.Div([
                                      html.H6("Energije danas: {}kW".format(df.iloc[-1,7]), style=style),
                                      html.H6("Energije u tjednu: {}kW".format(df.iloc[-1,8]), style=style),
                                      html.H6("Energije u mjesecu: {}kW".format(df.iloc[-1,9]), style=style),
                                      html.H6("Energije u godini: {}kW".format(df.iloc[-1,10]), style=style),
                                      html.H6("Energije ukupno: {}kW".format(df.iloc[-1,11]), style=style)], className='six columns')
                              ], className='row')
                    ])
            
@app.callback(Output('live-update-graph', 'figure'),
              [Input('my-interval', 'n_intervals')])
def update_graph(n):
    t1 = time.time()
    conn =  mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
    query = "SELECT * FROM elektrana"
    df = pd.read_sql(query, conn)
    data = {'Vrijeme':[],
            'Snaga_AC':[],
            'Snaga_DC':[],
            'Temp_kon':[]}
    for i in range(10):
        vrijeme = df.iloc[-(1+i),0]
        snaga_ac = df.iloc[-(1+i),2]
        snaga_dc = df.iloc[-(1+i),1]
        ucin = df.iloc[-(1+i),6]
        data['Vrijeme'].append(vrijeme)
        data['Snaga_AC'].append(snaga_ac)
        data['Snaga_DC'].append(snaga_dc)
        data['Temp_kon'].append(ucin)
    fig = plotly.tools.make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig['layout']['legend'] = {'x': 1, 'y': 1, 'xanchor': 'left'}
    fig['layout']['xaxis1'].update(title='Vrijeme')
    fig['layout']['yaxis1'].update(title='Snaga [W]')
    fig['layout']['yaxis2'].update(title='Temperatura [°C]')
    fig.append_trace({
        'x': data['Vrijeme'],
        'y': data['Snaga_AC'],
        'name': 'Snaga AC',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['Vrijeme'],
        'y': data['Snaga_DC'],
        'name': 'Snaga DC',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['Vrijeme'],
        'y': data['Temp_kon'],
        'name': 'Temperatura konvertera',
        'mode': 'lines+markers',
        'type': 'scatter',
        'marker': {'color':'green'}
    }, 2, 1)
    t2 = time.time()
    print('Vremena za update grafa: {}'.format(t2-t1))
    return fig

@app.callback(Output('tabs-content', 'children'),
              [Input('my-tabs', 'value'),
              Input('my-date-picker-range', 'start_date'),
              Input('my-date-picker-range', 'end_date')])
def render_content(tab, start_date, end_date):
    conn =  mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
    query = "SELECT * FROM elektrana WHERE Vrijeme >= '{} 06:00:00' AND Vrijeme <= '{} 20:00:00'".format(start_date, end_date)
    df = pd.read_sql(query, conn)
    if tab == 'tab-1':
        return html.Div([
                        html.H3('Testni prikaz sveukupne proizvodnje',
                                style={'color':'rgb(255,255,255)',
                                       'text-shadow':'1px 1px #000000',
                                       'text-align': 'center'}),
                        dcc.Graph(
                                 figure=go.Figure(
                                                 data=[
                                                      go.Scatter(
                                                                x=df['Vrijeme'],
                                                                y=df['Snaga_DC'],
                                                                name='Snaga DC'
                                                                ),
                                                      go.Scatter(
                                                                x=df['Vrijeme'],
                                                                y=df['Snaga_AC'],
                                                                name='Snaga AC'
                                                                )
                                                      ],
                                                 layout=go.Layout(
                                                                 title='Snaga (DC, AC)',
                                                                 showlegend=True,
                                                                 yaxis=dict(title='Snaga u W'),
                                                                 xaxis=dict(title='Vrijeme')
                                                                 )
                                                 ),
                                 style={'height': 550},
                                 id='my-graph'
                                 )
                        ])
    elif tab == 'tab-2':
        return html.Div([
                        html.H3('Podaci o prethodnoj proizvodnji',
                                style={'color':'rgb(255,255,255)',
                                       'text-shadow':'1px 1px #000000',
                                       'text-align': 'center'}),
                        dash_table.DataTable(
                                            id='table',
                                            columns=[{"name": i, "id": i} for i in df.columns],
                                            data=df.to_dict("rows")
                                            )                    
                        ])

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)