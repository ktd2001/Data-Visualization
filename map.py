# Import Modules 
import dash
import dash_table_experiments as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State


# Create tab name in browser
app = dash.Dash(__name__)
server = app.server
app.title = 'SF Restaurant Inspection Analysis'

# API key and datasets
mapbox_access_token = "pk.eyJ1Ijoia3RkMjAwMSIsImEiOiJjanUwZzBkZWYxYWdyNDRtcTB3M3Rqb2w2In0.HC_MMaor7bWiJEu7Ytp7pA"
map_data = pd.read_csv("20restuarnte.dat",parse_dates=True)
#df.head(10)

# Selecting desired columns
map_data = map_data[["business_name", "business_address", "business_latitude", "business_longitude", "inspection_date", "risk_category", "inspection_score", "business_state", "business_postal_code"]].dropna()
#map_data.head(5)

# Boostrap CSS
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

#Layout
#layout_table = dict(
#    autosize=True,
#    height=500,
#    font=dict(color="#191A1A"),
#    titlefont=dict(color="#191A1A", size='14'),
#    margin=dict(
#        l=35,
#        r=35,
#        b=35,
#        t=45
#    ),
#    hovermode="closest",
#    plot_bgcolor='#fffcfc',
#    paper_bgcolor='#fffcfc',
#    legend=dict(font=dict(size=10), orientation='h'),
#)
#layout_table['font-size'] = '12'
#layout_table['margin-top'] = '20'
        
   #Header layout
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
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        San Francsico Restaurant Inspection Analysis
                        ''',
                        className='nine columns'
                )
            ], className="row"
      ),
        
#Selectors
html.Div(
        [
            html.Div(
                [
                    html.P('Select Risk Category:'),
                    dcc.Checklist(
                            id = 'Category',
                            options=[
                                {'label': 'Low Risk', 'value': 'LR'},
                                {'label': 'Moderate Risk', 'value': 'MR'},
                                {'label': 'Hight Risk', 'value': 'HR'}
                            ],
                            values=['LR', 'MR', 'HR'],
                            labelStyle={'display': 'inline-block'}
                    ),
                ],
                className='six columns',
                style={'margin-top': '10'}
            ),
            html.Div(
                [
                    html.P('Zip Code:'),
                    dcc.Dropdown(
                        id='Zip_Code_Widget',
                        options= [{'label': int(item),
                                                'value': int(item)}
                                                for item in set(map_data['business_postal_code'])],
                        multi=True,
                        #value=list(set(map_data['business_postal_code']))
                    ),
                    dt.DataTable(
                        #rows=map_data.to_dict('records'),
                        rows=map_data.to_dict('rows'),
                        columns=map_data.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        id='datatable')
                ],
                className='six columns',
                style={'margin-top': '10'}
            )
   ],className='row'
),

], className='ten columns offset-by-one'))

# Server Startup #########################################################
if __name__ == "__main__":
    print('hello there map.py')
    app.run_server(debug=True)

#Callback
#Datatable callback
@app.callback(
    #dash.dependencies.Output('datatable', 'rows'),
    [
	dash.dependencies.Input('Zip_Code_Widget', 'values'),
    ])
def update_selected_row_indices(currently_selected_zipcode_values):
    print(currently_selected_zipcode_values)
    #map_aux = map_data.copy()

 # Zip Code filter
    #map_aux = map_aux[map_aux["business_postal_code"].isin(zipcode)]
 # Risk Category filter
    #map_aux = map_aux[map_aux["risk_category"].isin(category)]

    #rows = map_aux.to_dict('records')
    #return rows

