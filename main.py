# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Load the cleaned data
df = pd.read_csv('cleaned_data.csv', index_col=0)

map1_codes_titles = {'T01': 'Property Taxes', 'T09': 'General Sales and Gross Receipts Taxes',
                     'T10': 'Alcoholic Beverages Sales Tax', 'T16': 'Tobacco Products Sales Tax'}
map2_codes_titles = {'T24': 'Motor Vehicles License', 'T25': 'Motor Vehicle Operators License',
                     'T40': 'Individual Income Taxes', 'T41': 'Corporation Net Income Taxes'}


def create_map(item_code, title):
    data = df.loc[item_code]
    min_val = data.min()
    max_val = data.max() / 4

    fig = go.Figure(data=go.Choropleth(
        locations=data.index,
        z=data.astype(float),
        locationmode='USA-states',
        colorscale='Reds',
        zmin=min_val,
        zmax=max_val,
        colorbar_title="Millions USD",
    ))

    fig.update_layout(
        title_text=f'US State Tax Data for {title}',
        geo_scope='usa',  # Limit map scope to USA
    )

    return fig


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='map1-dropdown',
            options=[{'label': v, 'value': k} for k, v in map1_codes_titles.items()],
            value=list(map1_codes_titles.keys())[0]
        ),
        dcc.Graph(id='map1')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='map2-dropdown',
            options=[{'label': v, 'value': k} for k, v in map2_codes_titles.items()],
            value=list(map2_codes_titles.keys())[0]
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
    return create_map(map1_code, map1_codes_titles[map1_code]), create_map(map2_code, map2_codes_titles[map2_code])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
