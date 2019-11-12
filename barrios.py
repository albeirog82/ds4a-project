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

BINS = ['0-2', '2.1-4', '4.1-6', '6.1-8', '8.1-10', '10.1-12', '12.1-14', \
		'14.1-16', '16.1-18', '18.1-20', '20.1-22', '22.1-24',  '24.1-26', \
		'26.1-28', '28.1-30', '>30']
		
DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]		

cm = dict(zip(BINS, DEFAULT_COLORSCALE))

data = [dict(
			lat = df_lat_lon['latitude'],
			lon = df_lat_lon['longitude'], 
			text = df_lat_lon['text'], 
			type = 'scattermapbox',
			hoverinfo = 'text',
			marker = dict(size=5, color='white', opacity=0)
			)
		]
		
annotations = [dict(
	showarrow = False,
	align = 'right',
	text = '<b>Age-adjusted death rate<br>per county per year</b>',
	x = 0.95,
	y = 0.95,
)]

for i, bin in enumerate(reversed(BINS)):
	color = cm[bin]
	annotations.append(
		dict(
			arrowcolor = color,
			text = bin,
			x = 0.95,
			y = 0.85-(i/20),
			ax = -60,
			ay = 0,
			arrowwidth = 5,
			arrowhead = 0,
			bgcolor = '#EFEFEE'
		)
	)

for i, bin in enumerate(reversed(BINS)):
	color = cm[bin]
	annotations.append(
		dict(
			arrowcolor = color,
			text = bin,
			x = 0.95,
			y = 0.85-(i/20),
			ax = -60,
			ay = 0,
			arrowwidth = 5,
			arrowhead = 0,
			bgcolor = '#EFEFEE'
		)
	)
	
#if 'hide_legend' in map_checklist:
#	annotations = []	

#if 'layout' in figure:
#	lat = figure['layout']['mapbox']['center']['lat']
#	lon = figure['layout']['mapbox']['center']['lon']
#	zoom = figure['layout']['mapbox']['zoom']
#else:
#	lat = 4.6918154,
#	lon = -74.0765448,
#	zoom = 9.5

		
		
layout = dict(
	mapbox = dict(
		layers = [], 
		accesstoken = token, 
		style = 'light', 
		center=dict(
			lat=4.6918154,
			lon=-74.0765448), 
		pitch=0, 
		zoom=9.5
	), 
	hovermode = 'closest',
	margin = dict(r=0, l=0, t=0, b=0),
	annotations = annotations,
	dragmode = 'lasso'
)
#layout = dict(mapbox = dict(layers = dict(sourcetype = 'geojson',source = 'barrios_clock.geojson',type = 'fill',color = "#80d482",opacity = 0.8), accesstoken = token, style = 'light', center=dict(lat=4.6918154,lon=-74.0765448), pitch=0, zoom=10.5))

#dict(sourcetype = 'geojson',source = 'xbarrios_clock.geojson',type = 'fill',color = "#80d482",opacity = 0.8)

geo_layer = dict(
	sourcetype = 'geojson',
	source = 'https://raw.githubusercontent.com/albeirog82/ds4a-project/master/neigh.geojson',
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
	