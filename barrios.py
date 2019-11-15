from sqlalchemy import create_engine
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import random
from dash.dependencies import Input, Output, State
import json
from urllib.request import urlopen


app = dash.Dash(__name__)
token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

#with urlopen('https://raw.githubusercontent.com/albeirog82/ds4a-project/master/neigh.geojson') as response:
#    neigs = json.load(response)
with open('neigh_id.geojson') as f:
    geojson = json.loads(f.read())

neighs_data = pd.read_csv('neigh_data.csv', dtype={'id': object})

print(neighs_data.head())

app.layout = html.Div([
	html.Div(
        children=[
            html.H2(children="Bogota", className='h2-title'),
        ],
        className='study-browser-banner row'
    ),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Main', children=[
            html.Div([
				dcc.Graph(
					id = 'bogota-choropleth', 
					figure={ 
							'data': [go.Choroplethmapbox(
								geojson=geojson,
								locations=neighs_data['id'],
								text=neighs_data['neighborhood'],
								z=neighs_data['value'],
								colorscale='Viridis',
								colorbar_title="Values"
							)],
							'layout': go.Layout(
									mapbox_style="light",
									mapbox_accesstoken=token,
									mapbox_zoom=9,
									mapbox_center = {"lat": 4.6918154, "lon": -74.0765448}
							)
					}
				)
            ])
        ]),
        dcc.Tab(label='Index calculation', children=[
                dcc.Graph(
                    id='example-graph-1',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [1, 4, 1],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [1, 2, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
        ]),
        dcc.Tab(label='Neighborhood Review', children=[
                dcc.Graph(
                    id='example-graph-2',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
        ]),
		dcc.Tab(label='Compare', children=[
				dcc.Dropdown(
					options=[
						{'label': 'New York City', 'value': 'NYC'},
						{'label': 'Montréal', 'value': 'MTL'},
						{'label': 'San Francisco', 'value': 'SF'}
					],
					value='MTL'
				),  
				dcc.Dropdown(
					options=[
						{'label': 'New York City', 'value': 'NYC'},
						{'label': 'Montréal', 'value': 'MTL'},
						{'label': 'San Francisco', 'value': 'SF'}
					],
					value='MTL'
				), 				
                dcc.Graph(
                    id='example-graph-3',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
        ]),
    ])
])

#@app.callback(
#		Output('bogota-choropleth', 'figure'),
#		[State('bogota-choropleth', 'figure')])
def display_map():
	
	print("Start display")
	data = [dict(
		lat = df_lat_lon['Latitude '],
		lon = df_lat_lon['Longitude'],
		text = df_lat_lon['Hover'],
		type = 'scattermapbox',
		hoverinfo = 'text',
		#selected = dict(marker = dict(opacity=1)),
		#unselected = dict(marker = dict(opacity = 0)),
		marker = dict(size=5, color='white', opacity=0)
	)]
	
	layout = dict(
		mapbox = dict(
			layers = [],
			accesstoken = mapbox_access_token,
			style = 'light',
			center=dict(lat=lat, lon=lon),
			zoom=zoom
		),
		hovermode = 'closest',
		margin = dict(r=0, l=0, t=0, b=0),
		annotations = annotations,
		dragmode = 'lasso'
	)
	
	fig = dict(data=data, layout=layout)
	return fig

if __name__ == "__main__":
    app.run_server(debug=True)
	