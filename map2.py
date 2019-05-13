#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
#Column numbers with one indexing (1-10; t = 10)
#23456789t123456789t123456789t123456789t123456789t123456789t123456789t123456789t

# Import Modules 
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output


# Create tab name in browser
app = dash.Dash(__name__)
server = app.server
app.title = 'SF Restaurant Inspection Analysis'

# API key and datasets
mapbox_access_token = "pk.eyJ1Ijoia3RkMjAwMSIsImEiOiJjanUwZzBkZWYxYWdyNDRtcTB3M3Rqb2w2In0.HC_MMaor7bWiJEu7Ytp7pA"


# Read in all data
df = pd.read_csv('restaurant_scores.csv')
# Drop the rows containing NA
df = df.dropna()
# Drop rows in such a way as to retain only n randomly chosen rows (in this case n is set to 1000)
df = df.sample(n=1000)

df['text'] = df['business_name'] +"<br>"+ df['risk_category'] +"<br>"+ df['inspection_type']+"<br>"+ df['inspection_score'].astype(str)

# Color Scale and color variables
scl1 = [[0, 'red'],[0.5,"rgb(255, 255, 0)"], [1.0, 'green']]

scl2 = [[0, 'green'],[0.5,"rgb(255, 255, 0)"],[1.0,"rgb(255, 0, 0)"] ]

color_names= [' ','Low','Moderate','High']

color_vals = list(range(len(color_names)))

num_colors = len(color_vals)

# Created new columns turn strings into numbers 
def trans_risk_category(x):
    if x == 'Low Risk':
        return 1.0
    if x == 'Moderate Risk':
        return 2.0
    if x == 'High Risk':
        return 3.0
    
df['numerical_risk_category'] = df['risk_category'].apply(trans_risk_category) 


# Setting up figure 1
data1 = [
        go.Scattermapbox(
                        lon = df['business_longitude'],
                        lat = df['business_latitude'],
                        text = df['text'],
                        mode='markers',
                        marker=go.scattermapbox.Marker(
                                                      size=14,
                                                      colorscale = scl1,
                                                      opacity=0.50,
                                                      cmin = -0,
                                                      color = df['inspection_score'],
                                                      cmax = -100,
                                                      colorbar=dict(title="Inspection Score"),
                                                      )
                        )
        ]

layout1 = go.Layout(title='Map of Inspection Scores for SF Restaurants', 
		    autosize=False,
    		    width=1800,
                    height=500,
    	 	    hovermode='closest',
		    mapbox=dict(accesstoken=mapbox_access_token, 
		    center=dict(lat=37.759174, lon=-122.418116), 
		    style='dark',
		    zoom=11.0)
                   )

fig1 = go.Figure(data=data1, layout=layout1 )


# Setting up figure 2

data2 = [
        go.Scattermapbox(
                        lon = df['business_longitude'],
                        lat = df['business_latitude'],
                        text = df['text'],
                        mode='markers',
                        marker=go.scattermapbox.Marker(
						      size=14,
                                                      colorscale = scl2,
                                                      opacity=0.50,
                                                      cmin = 1,
                                                      color = df['numerical_risk_category'],
                                                      cmax = 3,
                                                      colorbar=dict(title="Risk Category",tickvals= color_vals, ticktext= color_names),
                                                      )
                        )
        ]

layout2 = go.Layout(title='Map of Risk Category of SF Restaurants', 
		    autosize=True,
    		    width=1800,
                    height=600,
    	 	    hovermode='closest',
		    mapbox=dict(accesstoken=mapbox_access_token, 
		    center=dict(lat=37.759174, lon=-122.418116), 
		    style='dark',
		    zoom=11.0)
                   )

fig2 = go.Figure(data=data2, layout=layout2 )

# Setting up figure 3

data3 = [go.Histogram(x=df['inspection_score'])]

layout3 = go.Layout(title='Histogram for Restaurant Inspection Score Distribution', 
                    autosize=False,
                    width=1800,
                    height=600,
                    bargap=0.01,
                    xaxis=go.layout.XAxis(title='Inspection Scores'),
                    yaxis=go.layout.YAxis(title='Count')
                    )

fig3 = go.Figure(data=data3, layout=layout3)


# Setting up figure 4

data4 = [go.Histogram(x=df['numerical_risk_category'])]

layout4 = go.Layout(title='Histogram for Restaurant Risk Category Distribution',
		    autosize=False,
                    width=1300,
                    height=600,
 		    bargap=0.002, 
                    xaxis=go.layout.XAxis(title='Risk Category: Low Risk = 1, Moderate Risk = 2, High Risk = 3'),
                    yaxis=go.layout.YAxis(title='Count')
                    )

fig4 = go.Figure(data=data4, layout=layout4)

# Boostrap CSS
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
        
#Header layout
#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
app.layout = html.Div([
                       html.Div([
                                html.H1(children='San Francisco Restaurant Visualization',
                                className='main plot'),
 	
                                #html.P(children="Created By: Keiana Dunn dunnk11@go.stockton.edu",
                                #className='three columns',
                                #style={
                                #      'height': '6%',
                                #      'width': '6%',
                                #      'float': 'right',
                                #      'position': 'relative',
                                #      'padding-top': 2,
                                #      'padding-right': 2
                                #       }),
                                html.Div(children='''Visualization of 1000 SF restaurant inspection results (randomly sampled from 53,000 records)'''
                                         ,className='nine columns')
                               	 ], style={'textAlign': "center"
                                          }),#className="row"
      	                      # ),
      	                     
        

#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
                       html.Div([ 

                                 dcc.Graph(id='graph1', figure=fig1)

				 ]),

#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
                       html.Div([ 

                                 dcc.Graph(id='graph3', figure=fig3) 

                                 ]),

#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
                       html.Div([ 

                                 dcc.Graph(id='graph2', figure=fig2) 

                                 ]),

#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789
                       html.Div([ 

                                 dcc.Graph(id='graph4', figure=fig4) 

                                 ]), 
           	       html.Div([

                   		 html.P('        Created by:Keiana Dunn       ', style = {'display': 'inline'}),
                    		 html.A('dunnk11@go.stockton.edu', href = 'mailto:dunnk11@go.stockton.edu')
                                 
				 ], className = "twelve columns",
                                   style = {'fontSize': 18, 'padding-top': 20}
                                 ), 
    


#Column numbers with zero indexing ( 0-9 )
#1234567890123456789012345678901234567890123456789012345678901234567890123456789

                      ], className='first row')



# Server Startup #########################################################
if __name__ == "__main__":
    print('hello there map2.py')
    app.run_server(debug=True,hostname='0.0.0.0',port=8050)
