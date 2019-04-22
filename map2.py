#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:50:06 2019

@author: ktd2001
"""
# -*- coding: utf-8 -*-
# Import Modules
import dash
import dash_table_experiments as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#import plotly.graph_objs from *
from dash.dependencies import Input, Output, State, Event

# Create tab name in browser
app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True
app.title = 'SF Resturante Inspection Analysis'

# API key and datasets
mapbox_access_token = 'pk.eyJ1Ijoia3RkMjAwMSIsImEiOiJjanUwZzBkZWYxYWdyNDRtcTB3M3Rqb2w2In0.HC_MMaor7bWiJEu7Ytp7pA'
map_data = pd.read_csv("20restuarnte.dat")
#df.head(10)

# Selecting desired columns
map_data = map_data[["business_name", "business_address", "business_latitude", "business_longitude", "inspection_date", "risk_category", "inspection_score", "business_state", "business_postal_code"]].drop_duplicates()
#map_data.head(5)

# Boostrap CSS
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

#Layouts
    #Table layouts for font and colors
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)

layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

   # Map layouts
layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='SF Resturante Inspection',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-122.419066,
            lat=37.759174
        ),
        zoom=10,
    )
)

# function
def gen_map(map_data):
     #groupby returns a dictionary mapping the values of the first field
     #'classification' onto a list of record dictionaries with that
     #classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['business_latitude']),
                "lon": list(map_data['business_longitude']),
                "hoverinfo": "text",
                "hovertext": [["business_name: {} <br>risk_category: {} <br>inspection_score: {}".format(i,j,k)]
                                for i,j,k in zip(map_data['business_name'], map_data['risk_category'],map_data['inspection_score'])],
                "mode": "markers",
                "name": list(map_data['business_name']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }

#Header
app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Maps and Tables',
                        className='nine columns'),
                html.Img(
                    src="https://stockton.edu/relations/brand-guide/images/official-stockton-logo-alternate1-display.png",
                    className='three columns',
                    style={
                        'height': '11%',
                        'width': '11%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 12,
                        'padding-right': 20
                    },
                ),
                html.Div(children='''
                        San Fransico Resturante Inspection Analysis
                        ''',
                        className='nine columns'
               )
            ], className="row"
        ),



# Selectors
html.Div(
    [
            html.Div(
                [
                    html.P('Select Risk Category:'),
                    dcc.Checklist(
                            id = 'category',
                            options=[
                                {'label': 'Low Risk', 'value': 'LR'},
                                {'label': 'Moderate Risk', 'value': 'MR'},
                                {'label': 'High Risk', 'value': 'HR'}
                            ],
                            values=['LR', 'MR', 'HR'],
                            labelStyle={'display': 'inline-block'}
                    ),
                ], className='six columns',
                style={'margin-top': '10'}
         ),
            html.Div(
                [
                    html.P('Zip Code:'),
                    dcc.Dropdown(
                        id = 'zip_code',
                        options= [{'label': int(item),
					      'value': int(item)}
                                             for item in set(map_data['business_postal_code'])],
                        multi=True,
                        value=list(set(map_data['business_postal_code']))
                    )
                ],
                className='six columns',
                style={'margin-top': '10'}
            )
 	           ],
               className='row'
           ),
# Map + table + Histogram
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='map-graph',
                                animate=True,
                                style={'margin-top': '20'})
                ], className = "six columns"
            ),
            html.Div(
                [
                    dt.DataTable(
                        rows=map_data.to_dict('records'),
                        columns=map_data.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        id='datatable'),
                ],
                style = layout_table,
                className="six columns"
            ),
            html.Div([
                    dcc.Graph(
                        id='bar-graph'
                    )
                ], className= 'twelve columns'
                ),
            html.Div(
                [
                    html.P('Keiana Dunn', style = {'display': 'inline'}),
                    html.A('dunnk11@go.stockton.edu', href = 'mailto:dunnk11@go.stockton.edu')
                ], className = "twelve columns",
                    style = {'fontSize': 18, 'padding-top': 20}
            )
        ], className="row"
    )
], className= 'ten columns offset-by-one'))

@app.callback(
    dash.dependencies.Output('datatable', 'rows'),
    [dash.dependencies.Input('zip_code', 'value')],
     [dash.dependencies.Input('category', 'values')])
def update_selected_row_indices(zip_code, category):
    map_aux = map_data.copy()

# Zip Code filter
    map_aux = map_aux[map_aux['business_postal_code'].isin(zip_code)]

# Risk Category filter
    map_aux = map_aux[map_aux['risk_category'].isin(category)]

    rows = map_aux.to_dict('records')
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)

