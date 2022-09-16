from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dcb
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
#external_stylesheets = [ 'https://codepen.io/chriddyp/pen/bWLwgP.css', { 'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css', 'rel': 'stylesheet', 'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO', 'crossorigin': 'anonymous' } ]
external_stylesheets = [dcb.themes.BOOTSTRAP]

app = Dash(__name__,external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1("Scatter Graph", style={'textAlign':'center', 'backgroundColor':'#A65387', 'width':'50%'}),
    dcc.Graph(id='scatter-graph-with-slider'),
    html.Br(),
    dcc.Graph(id='pie-graph-with-slider'),
    html.Br(),
    html.Label("Select x and y axis values"),
    html.Br(),
    html.Div([
        dcc.Dropdown(id='xaxis', options=[col for col in df.columns], style={'width':'50%'}, value='gdpPercap'),
        dcc.Dropdown(id='yaxis', options=[col for col in df.columns], style={'width':'50%'}, value='lifeExp')
    ], style={'display':'flex'}),
    html.Br(),
    dcc.Slider(id='year-slider',
               min=df['year'].min(),
               max=df['year'].max(),
               step=None,
               value=df['year'].min(),
               marks={str(year): str(year) for year in df['year'].unique()}

    ),
    dcc.RadioItems(options=[{'label': 'Linear', 'value': 'linear'},
                            {'label': 'Log', 'value': 'log'}],
                   value='linear',
                   id='xaxis-type',
                   inline=True),
    dcc.RadioItems(options=[{'label': 'Linear', 'value': 'linear'},
                            {'label': 'Log', 'value': 'log'}],
                   value='linear',
                   id='yaxis-type',
                   inline=True)
])

@app.callback([Output('scatter-graph-with-slider', 'figure'),
               Output('pie-graph-with-slider', 'figure')],
              [Input('xaxis', 'value'),
               Input('yaxis', 'value'),
               Input('year-slider', 'value'),
               Input('xaxis-type', 'value'),
               Input('yaxis-type', 'value')])
def update_graph(xaxis, yaxis, year, xaxis_type, yaxis_type):

    dff = df[df['year'] == year]
    fig1 = px.scatter(data_frame=dff, x=xaxis, y=yaxis, size='pop',
                     color='continent', hover_name='country', size_max=55,
                     height=600, title=f'{xaxis} vs {yaxis} for {year}')
    fig1.update_layout({'plot_bgcolor': 'LightSteelBlue'})
    fig1.update_xaxes(title=f'Scale: {xaxis_type}, Variable: {xaxis}', type=xaxis_type)
    fig1.update_yaxes(title=f'Scale: {yaxis_type}, Variable: {yaxis}',type=yaxis_type)

    fig2 = px.pie(data_frame=dff, values=xaxis, names=yaxis, )
    fig2.update_traces(textposition='inside')
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)