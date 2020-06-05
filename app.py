import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import math
import plotly.graph_objs as go

refractive_indexes = np.array([1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,2.0,3.0])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H1(children='Refraction characteristics'),

    html.H2(children='''
        Principles of computer communication
    '''),

    dcc.Graph(id='graph-with-slider'),

    html.Div(children=''),
    dcc.Slider(
        id='rf-slider',
        min=refractive_indexes[0],
        max=refractive_indexes[-1],
        value=refractive_indexes[0],
        marks={int(RI) if RI%1==0 else RI : str(RI) for RI in refractive_indexes},
        step=None
    ),
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('rf-slider', 'value')])
def update_figure(refInd):
    ref = 1 # refractive index of air
    inc_vis = refInd # refractive index of the medium for visible spectrum
    inc_mil = refInd*2/1.51 # rf of the medium for millimeter wavve
    crit_vis = math.degrees(math.asin(ref/inc_vis))
    crit_mil = math.degrees(math.asin(ref/inc_mil))
    refractive = [go.Bar(x=['visible light','millimeter wave'],y=[crit_vis,crit_mil])]
    return {
        'data': refractive,
        'layout': dict(
            xaxis={'title': 'wavelengths', 'auto-range': True},
            yaxis={'title': 'critical angle (degrees)', 'auto-range': True},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
