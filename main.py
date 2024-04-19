# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the cleaned data
df = pd.read_csv('cleaned_data.csv', index_col=0)

# Define the item codes for the two maps
map1_codes = ['T01', 'T09', 'T10', 'T16']
map2_codes = ['T24', 'T25', 'T40', 'T41']


# Define a function to create a choropleth map for a given item code
def create_map(item_code):
    data = df.loc[item_code]
    fig = go.Figure(data=go.Choropleth(
        locations=data.index, # Spatial coordinates
        z = data.astype(float), # Data to be color-coded
        locationmode = 'USA-states', # Set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Millions USD",
    ))

    fig.update_layout(
        title_text = f'US State Tax Data for {item_code}',
        geo_scope='usa', # Limit map scope to USA
    )

    return fig


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='map1-dropdown',
            options=[{'label': i, 'value': i} for i in map1_codes],
            value=map1_codes[0]
        ),
        dcc.Graph(id='map1')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='map2-dropdown',
            options=[{'label': i, 'value': i} for i in map2_codes],
            value=map2_codes[0]
        ),
        dcc.Graph(id='map2')
    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
])


# Define the callback for updating the maps
@app.callback(
    [Output('map1', 'figure'), Output('map2', 'figure')],
    [Input('map1-dropdown', 'value'), Input('map2-dropdown', 'value')]
)
def update_maps(map1_code, map2_code):
    return create_map(map1_code), create_map(map2_code)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
