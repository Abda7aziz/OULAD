import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json
import pyproj

# Import the layout from layout.py
from layout import layout

studentInfo_df = pd.read_csv('oulad/studentInfo_df.csv')
student_df = pd.read_csv('oulad/student_df.csv')
evaluation_df = pd.read_csv('oulad/evaluation.csv')


gdf = gpd.read_file('NUTS_Level_1_January_2018_GCB_in_the_United_Kingdom_2022_403493202252417583')
gdf.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

mapping_dict = {
    'North East (England)': 'North Region',
    'North West (England)': 'North Western Region',
    'Yorkshire and The Humber': 'Yorkshire Region',
    'East Midlands (England)': 'East Midlands Region',
    'West Midlands (England)': 'West Midlands Region',
    'East of England': 'East Anglian Region',
    'London': 'London Region',
    'South East (England)': 'South East Region',
    'South West (England)': 'South West Region',
    'Wales': 'Wales',
    'Scotland': 'Scotland',
    'Northern Ireland': 'Ireland'
}
gdf['nuts118nm'] = gdf['nuts118nm'].replace(mapping_dict)


app = dash.Dash(__name__, title='OULAD', external_stylesheets=[dbc.themes.CYBORG])
server = app.server

app.layout = layout

# Create callbacks for any interactive components or visualizations
# For example, if you want to update the choropleth map based on some input, create a callback here
@app.callback(
    Output('mStudents', 'children'),
    Output('fStudents', 'children'),
    Input('moduleDropdown', 'value'),
    Input('xAxisDropDown','value'),
    Input('barChart', 'selectedData'),
    Input('choroplethMap','selectedData'))
def sCards(module,x,bar,map):
    df = studentInfo_df.copy()
    if module != None:
        df = df[(df['code_module']==module.split('-')[0])&(df['code_presentation']==module.split('-')[1])]
    if bar != None:
        if len(bar['points']) == 1:
            df = df[df[x]==bar['points'][0]['x']]
        elif len(bar['points']) > 1:
            df = df[df[x].isin([bar['points'][i]['x'] for i in range(len(bar['points']))])]
    if map != None:
        if len(map['points']) == 1:
            df = df[df['region']==map['points'][0]['hovertext']]
        elif len(map['points']) > 1:
            df = df[df['region'].isin([map['points'][i]['hovertext'] for i in range(len(map['points']))])]


    df = df.groupby('gender')['id_student'].count().reset_index()
    return f"{df[df['gender'] == 'M']['id_student'].values[0]:,}",f"{df[df['gender'] == 'F']['id_student'].values[0]:,}"

@app.callback(
    Output('table', 'columns'),
    Output('table', 'data'),
    Input('moduleDropdown', 'value'),
    Input('xAxisDropDown','value'),
    Input('barChart', 'selectedData'),
    Input('choroplethMap','selectedData'))
def table(module,x,bar,map):
    df = evaluation_df.copy()
    if module != None:
        df = df[(df['code_module']==module.split('-')[0])&(df['code_presentation']==module.split('-')[1])]
    if bar != None:
        if len(bar['points']) == 1:
            df = df[df[x]==bar['points'][0]['x']]
        elif len(bar['points']) > 1:
            df = df[df[x].isin([bar['points'][i]['x'] for i in range(len(bar['points']))])]
    if map != None:
        if len(map['points']) == 1:
            df = df[df['region']==map['points'][0]['hovertext']]
        elif len(map['points']) > 1:
            df = df[df['region'].isin([map['points'][i]['hovertext'] for i in range(len(map['points']))])]
        
    df.drop(columns=['code_module','code_presentation'],inplace=True)
    df = df[['id_student','region','module','final_result','score','sum_click']]
    columns=[{'name': i, 'id': i} for i in df.columns.tolist()]
    data=df.to_dict('records')  
    
    return columns,data


@app.callback(
    Output('barChart','figure'),
    Input('moduleDropdown', 'value'),
    Input('xAxisDropDown','value'),
    Input('yAxisDropDown','value'),
    Input('choroplethMap','selectedData'))
def barChart(module,x,y,map):
    df = studentInfo_df.copy()
    if module != None:
        df = df[(df['code_module']==module.split('-')[0])&(df['code_presentation']==module.split('-')[1])]
    if map != None:
        if len(map['points']) == 1:
            df = df[df['region']==map['points'][0]['hovertext']]
        elif len(map['points']) > 1:
            df = df[df['region'].isin([map['points'][i]['hovertext'] for i in range(len(map['points']))])]
        
    education_order = [
    "No Formal Qualification",
    "Lower Than A Level",
    "A Level or Equivalent",
    "HE Qualification",
    "Post Graduate Qualification"]
    df['highest_education'] = pd.Categorical(df['highest_education'], categories=education_order, ordered=True)
    grouped = df.groupby([x,y])['id_student'].count().reset_index()
    fig = px.histogram(grouped,x=x, y='id_student',color=y)
    fig.update_layout(
        xaxis_title=x.replace('_',' ').capitalize(),
        yaxis_title="Frequency",
        barmode='group',
        template='plotly_dark',
        margin=dict(l=0, r=0, t=0, b=0),
        )
    return fig



@app.callback(
    Output('scatterPlot', 'figure'),
    Input('moduleDropdown', 'value'),
    Input('xAxisDropDown','value'),
    Input('barChart', 'selectedData'),
    Input('choroplethMap','selectedData'))
def sCards(module,x,bar,map):
    df = evaluation_df.copy()
    if module != None:
        df = df[df['module']==module]
        print(df.head())
    if bar != None:
        if len(bar['points']) == 1:
            df = df[df[x]==bar['points'][0]['x']]
        elif len(bar['points']) > 1:
            df = df[df[x].isin([bar['points'][i]['x'] for i in range(len(bar['points']))])]
    if map != None:
        if len(map['points']) == 1:
            df = df[df['region']==map['points'][0]['hovertext']]
        elif len(map['points']) > 1:
            df = df[df['region'].isin([map['points'][i]['hovertext'] for i in range(len(map['points']))])]
    fig = scatter_plot = px.scatter(
        df,
        x='sum_click',
        y='score',
        template='plotly_dark',
        color='final_result',
        category_orders={'final_result': ['Distinction','Pass','Withdrawn','Fail']},
        title='Number of Clicks vs. Final Assessment Scores by Module',
        labels={'sum_click': 'Number of Clicks', 'score': 'Final Assessment Scores'}
    )
    fig.update_layout(
                    xaxis=dict(title='Number of Clicks'),
                    yaxis=dict(title='Assessment Score'),
                    showlegend=True,
                    template='plotly_dark',
                    margin=dict(l=0, r=0, b=0),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

@app.callback(
    Output('areaPlot', 'figure'),
    Input('moduleDropdown', 'value'),
    Input('xAxisDropDown','value'),
    Input('barChart', 'selectedData'),
    Input('choroplethMap','selectedData'))
def sCards(module,x,bar,map):
    df = studentInfo_df.copy()
    if module != None:
        df = df[(df['code_module']==module.split('-')[0])&(df['code_presentation']==module.split('-')[1])]
    if bar != None:
        if len(bar['points']) == 1:
            df = df[df[x]==bar['points'][0]['x']]
        elif len(bar['points']) > 1:
            df = df[df[x].isin([bar['points'][i]['x'] for i in range(len(bar['points']))])]
    if map != None:
        if len(map['points']) == 1:
            df = df[df['region']==map['points'][0]['hovertext']]
        elif len(map['points']) > 1:
            df = df[df['region'].isin([map['points'][i]['hovertext'] for i in range(len(map['points']))])]
    df = df.groupby(['age_band', 'final_result'])['id_student'].count().reset_index()
    desired_order = ['Withdrawn','Fail','Pass','Distinction']
    df['final_result'] = pd.Categorical(df['final_result'], categories=desired_order, ordered=True)
    df = df.sort_values(by=['age_band', 'final_result'])
    fig = go.Figure()

    for result in df['final_result'].unique():
        result_data = df[df['final_result'] == result]
        fig.add_trace(go.Scatter(
            x=result_data['age_band'],
            y=result_data['id_student'],  # Convert to percentage
            mode='lines',
            stackgroup='one',
            name=result,
            groupnorm='percent'
            ))
    fig.update_layout(
                    xaxis=dict(title='Age Band'),
                    yaxis=dict(title='Percentage of Students'),
                    showlegend=True,
                    template='plotly_dark',
                    margin=dict(l=0, r=0, t=0, b=0),
                    title='Distribution of Final Results across Age Bands',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig







@app.callback(
    Output('choroplethMap', 'figure'),
    Input('moduleDropdown', 'value'),
    Input('xAxisDropDown','value'),
    Input('barChart', 'selectedData'))
def choroplethMap(module,x,bar):
    df = studentInfo_df.copy()
    if module != None:
        df = df[(df['code_module']==module.split('-')[0])&(df['code_presentation']==module.split('-')[1])]
    if bar != None:
        if len(bar['points']) == 1:
            df = df[df[x]==bar['points'][0]['x']]
        elif len(bar['points']) > 1:
            df = df[df[x].isin([bar['points'][i]['x'] for i in range(len(bar['points']))])]
            
    df = gdf.merge(df.groupby('region')['id_student'].count().reset_index(),left_on='nuts118nm',right_on='region',how='right')
    data = [go.Choroplethmapbox(
    geojson=json.loads(df.geometry.to_json()),
    locations=df.index,
    hovertext=df['region'], 
    z=df['id_student'], 
    colorscale='teal',
    colorbar_title='Students')]
    data.append(go.Scattergeo(locations=df.index, text=df['id_student'], mode="text"))

    layout=go.Layout(mapbox_style="carto-darkmatter", mapbox_center = {"lat": 55.5, "lon": -2.5},
                  mapbox_zoom=4.8,template='plotly_dark',margin=dict(l=0, r=0, t=20, b=0),  
    uniformtext=dict(minsize=8, mode='hide'),geo={'fitbounds':'locations','visible':False},

    )

    return go.Figure(data=data,layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)


# @app.callback(
#     Output('boxPlot', 'figure'),
#     Input('moduleDropdown', 'value'),
#     Input('barChart', 'selectedData'),
#     Input('choroplethMap','clickData'))
# def sCards(module,bar,map):
#     students = evaluation_df.copy()
#     if bar != None:
#         pass
#     if map != None:
#         pass
#     if module != None:
#         students = students[(students['code_module']==module.split('-')[0])&(students['code_presentation']==module.split('-')[1])]
#     fig = box_plot = px.box(
#         students,
#         x='age_band',
#         y='sum_click',
#         # range_y=[0,10000],
#         category_orders={'age_band': ['0-35', '35-55', '55<=']},
#         template='plotly_dark',
#         labels={'score': 'Final Assessment Scores', 'sum_click': 'Number of Clicks'}
#     )
#     fig.update_layout(
#                     xaxis=dict(title='Age Band'),
#                     yaxis=dict(title='Number of Clicks'),
#                     showlegend=True,
#                     template='plotly_dark',
#                     margin=dict(l=0, r=0, b=0),
#                     # title='F'
#                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
#     return fig