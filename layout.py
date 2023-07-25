from dash import html,dcc,dash_table
import dash_bootstrap_components as dbc

header = html.Div(
    [
        html.H1("Student Data Analysis", className="display-3"),
        dbc.Row([
        dbc.Col(html.P("Open University Learning Analytics Dataset (OULAD)", className="lead"),width=3,style={'display': 'flex','align-items': 'left'}),
        dbc.Col(dcc.Dropdown(placeholder='All Modules',id='moduleDropdown',
            options=[{'label':i,'value':i}
                    for i in ['AAA-2013J','AAA-2014J','BBB-2013B','BBB-2013J','BBB-2014B','BBB-2014J','CCC-2014B',
                                'CCC-2014J','DDD-2013B','DDD-2013J','DDD-2014B','DDD-2014J','EEE-2013J','EEE-2014B',
                                'EEE-2014J','FFF-2013B','FFF-2013J','FFF-2014B','FFF-2014J','GGG-2013J','GGG-2014B','GGG-2014J']],
                    style={'width':'100%'}),width=2,style={'display': 'flex','align-items': 'left'})
        ]),
        html.Div(id='dummy',hidden=True)
    ],
className='mb-3')
# charts
barChart = dcc.Loading(dcc.Graph(id='barChart'))
choroplethMap = dcc.Loading(dcc.Graph(id='choroplethMap',style={'height':'850px'}))
boxPlot = dcc.Loading(dcc.Graph(id='boxPlot'))
scatterPlot = dcc.Loading(dcc.Graph(id='scatterPlot',clear_on_unhover=True))
areaPlot = dcc.Loading(dcc.Graph(id='areaPlot',style={'height':'353px'}))

row1 = dbc.Row([
    dbc.Col([
        dbc.Row([
        dbc.Col(dbc.Card([html.H4('Male Students',className='blue-c'),dcc.Loading(html.H2(id='mStudents',style={'display': 'flex','justify-content':'center'}))],className='card')),
        dbc.Col(dbc.Card([html.H4('Female Students',className='red-c'),dcc.Loading(html.H2(id='fStudents',style={'display': 'flex','justify-content':'center'}))],className='card'))
        ],className='mb-3'),
        dbc.Row(dbc.Col(dbc.Card(dcc.Loading(dash_table.DataTable(id='table',page_size=9,
                                style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white'},
                                style_data={'backgroundColor': 'rgb(20, 20, 20)','color': 'white'},
                                css=[{ 'selector': '.current-page', 'rule': 'background-color: white;'}])),
                                 className='card')))
        ],width=5),
    
    
    dbc.Col(dbc.Card([
        dbc.Row([
            dbc.Col([
                html.P('X Axis',className='m-0'),
                dcc.Dropdown(id='xAxisDropDown',value='imd_band',clearable=False,
                            options=[{'label':i.replace('_',' ').capitalize(),'value':i} for i in ['age_band','imd_band','gender','highest_education']])
                ],width=3),
            dbc.Col([
                html.P('Y Axis',className='m-0'),
                dcc.Dropdown(id='yAxisDropDown',value='highest_education',clearable=False,
                            options=[{'label':i.replace('_',' ').capitalize(),'value':i} for i in ['age_band','imd_band','gender','highest_education']])
                ],width=3),
            dbc.Col(width=6)],className='mx-3'),
            barChart
        ],className='card'),
    width=7)],className='mb-4')

row2 = dbc.Row([
        dbc.Col([dbc.Card(scatterPlot,className='card mb-3'),
                 dbc.Card(areaPlot,className='card'),
                 ],width=8),
        dbc.Col(dbc.Card(choroplethMap,className='card',style={'height':'100%'}),width=4)
    ])

layout = dbc.Container(
    [
        header,
        row1,
        row2
    ]
)
