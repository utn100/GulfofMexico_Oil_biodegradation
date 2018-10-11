import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import base64


app = dash.Dash()
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
server = app.server

markdown_text = '''
#### **Project Introduction**

  A significant portion of oil released during the Deepwater Horizon disaster reached the Gulf of Mexico (GOM) seafloor.
Predicting the long-term fate of this oil is hindered by a lack of data about the combined influences of pressure,
temperature, and sediment composition on microbial hydrocarbon remineralization in deep-sea sediments.

  To investigate crude oil biodegradation by native GOM microbial communities,
we incubated core-top sediments from 13 GOM sites at water depths from 60-1500 m
with crude oil under simulated aerobic seafloor conditions.

  After 18 days, samples were extracted for oil organic matter to measure the extent of oil depletion,
and for DNA to investigate microbial communities associated with oil biodegradation.

  Hover mouse over points to see plots.
'''

df = pd.read_csv('Data/Oil_DNA_map.csv')
compounds = ['n-alkanes','PAHs']
colors = {'n-alkanes':'#ff8d00','PAHs':'#00d6f7'}

scl = [0,"rgb(0, 0, 200)"],[200,"rgb(0, 25, 255)"],\
[400,"rgb(0, 152, 255)"],[600,"rgb(44, 255, 150)"],[800,"rgb(151, 255, 0)"],\
[1000,"rgb(255, 234, 0)"],[1200,"rgb(255, 111, 0)"],[1400,"rgb(255, 0, 0)"]

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())



app.layout = html.Div([
                html.H2("Investigate oil biodegradation on the Gulf of Mexico seafloor",style={'text-align': 'center','color':'red'}),
                html.Div([
                html.Div([
                    dcc.Graph(id='graph',
                            figure = {'data':[ dict(
                                    type = 'scattergeo',
                                    location = 'GOM',
                                    lon = df['Lon'],
                                    lat = df['Lat'],
                                    text = 'Site: '+df['Site'] + ', at '+df['WD'].astype(str) + ' m' + ' water depth'
                                        + '<br>'+ 'TOC: ' + round(df['TOC'],2).astype(str) +' (wt%)'
                                        + '<br>'+ 'Carbonate content: ' + round(df['Carb'],2).astype(str) +' (wt%)',
                                    mode = 'markers',
                                    marker = dict(
                                        size = 7,
                                        opacity = 0.7,
                                        color = df['color'],
                                        #colorscale = 'scl',
                                        #reversescale = True,
                                        #autocolorscale = False,
                                        symbol = 'circle',
                                        line = dict(width=1,color='rgba(102, 102, 102)')))],
                                    'layout': dict(
                                            title = 'Northern Gulf of Mexico sample map',
                                            geo = dict(
                                            scope = 'north america',
                                            showland = True,
                                            landcolor = "rgb(212, 212, 212)",
                                            subunitcolor = "rgb(255, 255, 255)",
                                            countrycolor = "rgb(255, 255, 255)",
                                            showlakes = True,
                                            lakecolor = "rgb(255, 255, 255)",
                                            showsubunits = True,
                                            showcountries = True,
                                            resolution = 50,
                                            projection = dict(
                                                type = 'conic conformal',
                                                rotation = dict(
                                                    lon = -100)),
                                            lonaxis = dict(
                                                showgrid = True,
                                                gridwidth = 0.5,
                                                range= [ -97, -79.5 ],
                                                dtick = 5),
                                            lataxis = dict (
                                                showgrid = True,
                                                gridwidth = 0.5,
                                                range= [ 26.0, 34.0 ],
                                                dtick = 5)),
                                            autosize=True,
                                            height=500,
                                            font=dict(color='#f7f8fc'),
                                            titlefont=dict(color='#f7f8fc', size='22'),
                                            margin=dict(l=50,r=35,b=35,t=45),
                                            hovermode="closest",
                                            plot_bgcolor="#191A1A",
                                            paper_bgcolor="#2F2F2F"
                                            )})],className='seven columns'),
                                    html.Div([
                                        dcc.Markdown(children=markdown_text)],className='five columns',
                                                style={'fontSize':14,'color':'#f7f8fc','background': '#2F2F2F','height':500,'margin-left':'10'})
                                            ], className='row',style={'margin-top': '10'}),
        html.Div([
                html.Div([
                html.Img(id='hover-image-1',  src='children',height=400)
                ], className='seven columns', style={'margin-top': '20'}),
                html.Div([
                dcc.Graph(id='hover-image-2')
                ], className='five columns', style={'margin-top': '10','margin-left':'10'})
                ],className='row')
])

@app.callback(Output('hover-image-1','src'),
            [Input('graph','hoverData')])


def callback_image(hoverData):
    if hoverData is None:
        lon = df['Lon'].iloc[0]
        lat = df['Lat'].iloc[0]
    else:
        lon = hoverData['points'][0]['lon']
        lat = hoverData['points'][0]['lat']
    #pointIndex = hoverData['points'][0]['pointIndex']
    path = 'Web_figs/'

    return encode_image(path+df[(df['Lon']==lon)&(df['Lat']==lat)]['Image_file'].iloc[0])

@app.callback(Output('hover-image-2','figure'),
            [Input('graph','hoverData')])

def callback_barchart(hoverData):
    if hoverData is None:
        lon = df['Lon'].iloc[0]
        lat = df['Lat'].iloc[0]
    else:
        lon = hoverData['points'][0]['lon']
        lat = hoverData['points'][0]['lat']
    sub_df = df[(df['Lon']==lon)&(df['Lat']==lat)]
    data = []
    for compound in compounds:
        trace = go.Bar(
            x=sub_df['Group'],  # NOC stands for National Olympic Committee
            y=round(sub_df[compound],1),
            name = compound,
            marker=dict(color=colors[compound]) # set the marker color to gold
        )
        data.append(trace)


    layout = go.Layout(
        title='Oil compound depletion (%)',
        plot_bgcolor="#191A1A",
        paper_bgcolor="#2F2F2F",
        font=dict(color='#f7f8fc'),
        hovermode='closest',
        xaxis={'title':'Sample'},
        yaxis={'title':'Depletion %'}
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server()
