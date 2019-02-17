import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import pymysql as mysql

app = dash.Dash(__name__)

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
                        html.Div(id='content'),
                        dcc.Location(id='location', refresh=False),
                        html.Div(
                                html.H2('Test for a graph.')),
                        html.Div(
                                dcc.Graph(id='live_graph', animate=True),
                                dcc.Interval(id='graph_update', interval=10000, n_intervals=0)           
)])

@app.callback(Output('live_graph', 'figure'), [Input('graph_update', 'n_intervals')])
def update_graph():
        
    #Konekcija s bazom podataka.
    conn =  mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
    
    query = "SELECT * FROM elektrana"
    df = pd.read_sql(query, conn)
            
    data = go.Scatter(
            x = list(df['Vrijeme'][-1:-50]),
            y = list(df['Snaga_AC'][-1:-50]),
            mode='lines+markers',
            name='Proba')
    return {'data': [data], 'layout': go.Layout(xaxis = dict(range=[df['Vrijeme'][0], df['Vrijeme'][-1]]),
                                                yaxis = dict(range=[df['Snaga_AC'][0], df['Snaga_AC'][-1]]))}

if __name__ == '__main__':
    app.run_server(debug=True)