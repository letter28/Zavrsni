import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dash Tutorials'),
    dcc.Graph(id='example',
              figure={
                      'data': [{'x': 1, 'y': 1, 'type': 'line', 'name': 'Snaga'}],
                      'layout': {'title': 'Basic Dash Example'}
        }),
    dcc.Graph(id='napon_mreze')
])

if __name__ == '__main__':
    app.run_server(debug=True)