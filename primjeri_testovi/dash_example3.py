import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import pymysql as mysql

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
   [
    html.Div([
       html.Div([
          html.H1(children='PERFORMANCE REPORT AUGUST',
            style={
            'color':'#36A9DE'
                    }, className='nine columns'),
            html.Div(children='''*Created using Plotly Dash Python framework''',
                    className='nine columns'
                    )
                ], className="row"
            )
        ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id='example-graph'
                )], className='six columns'
                )
            ], className='row'
            )
   ]
)
@app.callback(Output('example-graph', 'figure'))
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