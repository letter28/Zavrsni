import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
import pandas as pd
import pymysql as mysql
import urllib.parse as urllib
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def serve_layout():
    return (
    html.Div([
            html.H2('Fotonaponska elektrana FN1-Riteh: Podaci o proizvodnji', 
                    style={'color': 'rgb(255,255,255)',
                           'text-align': 'center',
                           'text-shadow':'1px 1px #000000'}),
            html.Div(id='live-update-text'),
            dcc.Graph(id='live-update-graph'),
            dcc.Tabs(id="my-tabs", value='tab-1-example', children=[
                                                                    dcc.Tab(label='Grafički prikaz prethodne proizvodnje', value='tab-1'),
                                                                    dcc.Tab(label='Tablica s podacima o proizvodnji', value='tab-2')
                                                                    ]),
            html.Div([
                    html.H5('Odaberi vremenski raspon:', style={'color': 'rgb(255,255,255)'}),
                    dcc.DatePickerRange(
                                       id='my-date-picker-range',
                                       min_date_allowed=dt(2019, 3, 6),
                                       max_date_allowed=dt.now(),
                                       initial_visible_month=dt(2019, 3, 2),
                                       start_date='2019-03-06',
                                       end_date='{}'.format(dt.now().date())
                                       ),
                    html.Div([html.A('Preuzmi podatke',
                                     id='download-link',
                                     download="Podaci.csv",
                                     href="",
                                     target="_blank",
                                     style={'color':'#FFFFFF'})])            
                      ], style={'text-align':'center',
                                'margin-right': 20}),
            html.Div(id='tabs-content'),
            dcc.Interval(id='my-interval', 
                         interval=45*1000, 
                         n_intervals=0),
            html.P('Izradio: Leon Kvež za Tehnički fakultet u Rijeci, veljača 2019.', style={'text-align':'right'})
             ], style={'background':'#4c4c4a',
                       'font-family':"Verdana"})
            )

app.layout = serve_layout

@app.callback(Output('live-update-text', 'children'),
              [Input('my-interval', 'n_intervals')])
def update_text(n):
    conn =  mysql.connect(host='pfw0ltdr46khxib3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                      user='kfd7pprqwrvy9uep',
                      password='zvg9opaacxqy4mmu',
                      db='oha3los99548olek')
    query = "SELECT * FROM elektrana"
    df = pd.read_sql(query, conn)
    style={'color':'rgb(255,255,255)', 'text-align':'center'}
    return html.Div([html.H4('Live podaci - korak 45 sek.:', style=style),
                    html.Div([
                             html.Div([
                                      html.P("Vrijeme: {}".format(df.iloc[-1,0]), style=style),
                                      html.P("Snaga AC: {} W".format(df.iloc[-1,2]), style=style),
                                      html.P("Snaga DC: {} W".format(df.iloc[-1,1]), style=style),
                                      html.P("Učinkovitost: {}%".format(df.iloc[-1,3]), style=style),
                                      html.P("Max. snaga danas: {} W".format(df.iloc[-1,4]), style=style),
                                      html.P("Frekvencija mreže: {} Hz".format(df.iloc[-1,5]), style=style),
                                      html.P("Temp. konvertera: {}°C".format(df.iloc[-1,6]), style=style)],className='four columns'),
                             html.Div([
                                      html.P('Proizvedeno:', style=style),
                                      html.P("Energije danas: {} kWh".format(df.iloc[-1,7]), style=style),
                                      html.P("Energije u tjednu: {} kWh".format(df.iloc[-1,8]), style=style),
                                      html.P("Energije u mjesecu: {} kWh".format(df.iloc[-1,9]), style=style),
                                      html.P("Energije u godini: {} kWh".format(df.iloc[-1,10]), style=style),
                                      html.P("Energije ukupno: {} kWh".format(df.iloc[-1,11]), style=style),
                                      html.P("Ušteda emisija CO2: {} T CO2".format(df.iloc[-1,11]*0.024), style=style)], className='four columns'),
                             html.Div([
                                      html.P('Meteorološki podaci:', style=style),
                                      html.P("Temperatura: {} °C".format(df.iloc[-1,12]), style=style),
                                      html.P("Smjer i brzina vjetra: {} m/s".format(df.iloc[-1,13]), style=style),
                                      html.P("Stanje vremena: {} ".format(df.iloc[-1,14]), style=style)], className='four columns')
                              ], className='row')
                    ])
            
@app.callback(Output('live-update-graph', 'figure'),
              [Input('my-interval', 'n_intervals')])
def update_graph(n):
    conn =  mysql.connect(host='pfw0ltdr46khxib3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                      user='kfd7pprqwrvy9uep',
                      password='zvg9opaacxqy4mmu',
                      db='oha3los99548olek')
    query = "SELECT * FROM elektrana"
    df1 = pd.read_sql(query, conn)
    data = {'Vrijeme':[],
            'Snaga_AC':[],
            'Snaga_DC':[],
            'Temp_kon':[]}
    for i in range(80):
        vrijeme = df1.iloc[-(1+i),0]
        snaga_ac = df1.iloc[-(1+i),2]
        snaga_dc = df1.iloc[-(1+i),1]
        temp_kon = df1.iloc[-(1+i),6]
        data['Vrijeme'].append(vrijeme)
        data['Snaga_AC'].append(snaga_ac)
        data['Snaga_DC'].append(snaga_dc)
        data['Temp_kon'].append(temp_kon)
    fig = plotly.tools.make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig['layout']['legend'] = {'x': 1, 'y': 1, 'xanchor': 'left'}
    fig['layout']['xaxis1'].update(title='Vrijeme')
    fig['layout']['yaxis1'].update(title='Snaga [W]')
    fig['layout']['yaxis2'].update(title='Temperatura [°C]')
    fig['layout']['height'] = 600
    fig['layout']['title'] = {'text':'Snaga AC/DC, Temperatura konvertera'}
    fig['layout']['plot_bgcolor'] = '#4c4c4a'
    fig['layout']['paper_bgcolor'] = '#4c4c4a'
    fig['layout']['font'] = {'color':'#e98400'}
    fig.append_trace({
        'x': data['Vrijeme'],
        'y': data['Snaga_AC'],
        'name': 'Snaga AC',
        'mode': 'lines+markers',
        'type': 'scatter',
    }, 1, 1)
    fig.append_trace({
        'x': data['Vrijeme'],
        'y': data['Snaga_DC'],
        'name': 'Snaga DC',
        'mode': 'lines+markers',
        'type': 'scatter',
    }, 1, 1)
    fig.append_trace({
        'x': data['Vrijeme'],
        'y': data['Temp_kon'],
        'name': 'Temperatura konvertera',
        'mode': 'lines+markers',
        'type': 'scatter',
        'marker': {'color':'green'}
    }, 2, 1)
    return fig

@app.callback(Output('tabs-content', 'children'),
              [Input('my-tabs', 'value'),
              Input('my-date-picker-range', 'start_date'),
              Input('my-date-picker-range', 'end_date')])
def render_content(tab, start_date, end_date):
    conn =  mysql.connect(host='pfw0ltdr46khxib3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                      user='kfd7pprqwrvy9uep',
                      password='zvg9opaacxqy4mmu',
                      db='oha3los99548olek')
    query = "SELECT * FROM elektrana WHERE Vrijeme >= '{} 05:00:00' AND Vrijeme <= '{} 21:00:00'".format(start_date, end_date)
    df2 = pd.read_sql(query, conn)
    if tab == 'tab-1':
        return html.Div([
                        html.H3('Prikaz sveukupne proizvodnje',
                                style={'color':'rgb(255,255,255)',
                                       'text-shadow':'1px 1px #000000',
                                       'text-align': 'center',
                                       'font-family':"Verdana"}),
                        dcc.Graph(
                                 figure=go.Figure(
                                                 data=[
                                                      go.Scatter(
                                                                x=df2['Vrijeme'],
                                                                y=df2['Snaga_DC'],
                                                                name='Snaga DC'
                                                                ),
                                                      go.Scatter(
                                                                x=df2['Vrijeme'],
                                                                y=df2['Snaga_AC'],
                                                                name='Snaga AC'
                                                                )
                                                      ],
                                                 layout=go.Layout(
                                                                 title='Snaga (DC, AC)',
                                                                 font=dict(color='#e98400'),
                                                                 showlegend=True,
                                                                 yaxis=dict(title='Snaga u W'),
                                                                 xaxis=dict(title='Vrijeme'),
                                                                 plot_bgcolor='#4c4c4a',
                                                                 paper_bgcolor='#4c4c4a'
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
                                       'text-align': 'center',
                                       'font-family':"Verdana"}),
                        dash_table.DataTable(
                                            id='table',
                                            columns=[{"name": i, "id": i} for i in df2.columns],
                                            data=df2.to_dict("rows"),
                                            sorting=True,
                                            style_cell={'textAlign': 'right',
                                                        'color':'rgb(255,255,255)',
                                                        'backgroundColor': '#4c4c4a'},
                                            style_cell_conditional=[{'if': {'row_index': 'odd'},
                                                                    'backgroundColor': '#5c5c5a'},
                                                                    {'if': {'column_id': 'Vrijeme'},
                                                                     'textAlign': 'center'},
                                                                   ],
                                            style_header={'backgroundColor': '#4c4c4a',
                                                          'fontWeight': 'bold',
                                                          'textAlign':'center'},
                                            style_data={'whiteSpace': 'normal'},
                                            css=[{'selector': '.dash-cell div.dash-cell-value',
                                                  'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}]
                                            )                    
                        ])

@app.callback(dash.dependencies.Output('download-link', 'href'),
              [Input('my-date-picker-range', 'start_date'),
               Input('my-date-picker-range', 'end_date')])
def update_download_link(start_date, end_date):
    conn =  mysql.connect(host='pfw0ltdr46khxib3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                      user='kfd7pprqwrvy9uep',
                      password='zvg9opaacxqy4mmu',
                      db='oha3los99548olek')
    query = "SELECT * FROM elektrana WHERE Vrijeme >= '{} 04:00:00' AND Vrijeme <= '{} 22:00:00'".format(start_date, end_date)
    dff = pd.read_sql(query, conn)
    csv_string = dff.to_csv(encoding='utf-8', date_format='%Y-%m-%d %H:%M:%S')
    csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string)
    return csv_string
    
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True, processes=4)