# Import required libraries
# data frame import cmd: wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id = 'site-dropdown', options =[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value' : 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value' : 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value' : 'KSC LC-39A'},
                                    {'label': '', 'value' : 'KSC LC-39A'}]
                                    ,value='ALL', placeholder="Select a launch site", searchable= True),
                            

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id = 'payload-slider',
                                                min = 0, max = 10000, step = 1000,
                                                marks = {0: '0',
                                                         2000: '2000',
                                                         4000: '4000',
                                                         6000: '6000',
                                                         8000: '8000',
                                                         10000: '10000'
                                                         },
                                                value = [min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                            
])
app.css.append_css({'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    bins = pd.get_dummies(spacex_df['Launch Site'])
    outcome = pd.concat([bins.reset_index(drop = True), spacex_df['class'].reset_index(drop = True)], axis = 1)
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title="All launch site's success rate")
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            fig = px.pie(outcome, values = 'class',
            names = 'CCAFS LC-40',
            title = 'CCAFS LC-40 - Success rate')
            return fig
        if entered_site == 'CCAFS SLC-40':
            fig = px.pie(outcome, values = 'class',
            names = 'CCAFS SLC-40',
            title = 'CCAFS SLC-40 - Success rate')
            return fig
        if entered_site == 'KSC LC-39A':
            fig = px.pie(outcome, values = 'class',
            names = 'KSC LC-39A',
            title = 'KSC LC-39A - Success rate')
            return fig
        else: 
            fig = px.pie(outcome, values = 'class',
            names = 'VAFB SLC-4E',
            title = 'VAFB SLC-4E - Success rate')
            return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    spacex_df['Payload Mass (kg)'] = spacex_df['Payload Mass (kg)'].astype(int)
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df[mask], x = 'Payload Mass (kg)' , y = 'class', color="Booster Version Category", title = 'All sites')
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            fig = px.scatter(spacex_df[mask][spacex_df[mask]['Launch Site'] == 'CCAFS LC-40'], x = 'Payload Mass (kg)' , y = 'class', color="Booster Version Category", title = 'CCAFS LC-40')
            return fig
        if entered_site == 'CCAFS SLC-40':
            fig = px.scatter(spacex_df[mask][spacex_df[mask]['Launch Site'] == 'CCAFS SLC-40'], x =  'Payload Mass (kg)', y = 'class', color="Booster Version Category" , title = 'CCAFS SLC-40')
            return fig
        if entered_site == 'KSC LC-39A':
            fig = px.scatter(spacex_df[mask][spacex_df[mask]['Launch Site'] == 'KSC LC-39A'], x =  'Payload Mass (kg)', y = 'class', color="Booster Version Category", title = 'KSC LC-39A')
            return fig
        else:
            fig = px.scatter(spacex_df[mask][spacex_df[mask]['Launch Site'] == 'VAFB SLC-4E'], x =  'Payload Mass (kg)', y = 'class', color="Booster Version Category", title = 'VAFB SLC-4E')
            return fig
    
# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
