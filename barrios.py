from sqlalchemy import create_engine
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import random
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

YEARS = [2003, 2004, 2005, 2006, 2007, \
		2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]

token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'


df_lat_lon = pd.read_csv('mockdata.csv')

data = [dict(lat = df_lat_lon['latitude'],lon = df_lat_lon['longitude'], text = df_lat_lon['text'], type = 'scattermapbox')]
layout = dict(mapbox = dict(layers = [], accesstoken = token, style = 'light', center=dict(lat=4.6918154,lon=-74.0765448), pitch=0, zoom=10.5))
#layout = dict(mapbox = dict(layers = dict(sourcetype = 'geojson',source = 'barrios_clock.geojson',type = 'fill',color = "#80d482",opacity = 0.8), accesstoken = token, style = 'light', center=dict(lat=4.6918154,lon=-74.0765448), pitch=0, zoom=10.5))

#dict(sourcetype = 'geojson',source = 'xbarrios_clock.geojson',type = 'fill',color = "#80d482",opacity = 0.8)

geo_layer = dict(
	sourcetype = 'geojson',
	source = 'https://case-5-1-ag.s3.us-east-2.amazonaws.com/0-2.geojson',
	type = 'fill', 
	color = "#80d482",
	opacity = 0.8)

layout['mapbox']['layers'].append(geo_layer)

print(layout)


print(df_lat_lon.head())

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H2(children="Bogota", className='h2-title'),
        ],
        className='study-browser-banner row'
    ),
	dcc.Slider(
					id='years-slider',
					min=min(YEARS),
					max=max(YEARS),
					value=min(YEARS),
					marks={str(year): str(year) for year in YEARS},
				),
    dcc.Graph(
        id = 'bogota-choropleth', 
		figure = dict(
				data = data,
				layout = layout
		)
    )
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
	