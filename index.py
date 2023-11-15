from dash import dcc
from dash import html
from dash import dash_table
from app import app

import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import Dash
from dash import Dash,no_update
import plotly.express as px
from dash import Dash, html, Input, Output, callback,State
from datetime import datetime as dt
from datetime import date
import pandas as pd
import numpy as np
import time
import urllib
# import dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from operator import itemgetter
import plotly.graph_objs as go
#from dash_extensions import Download
from dash.exceptions import PreventUpdate
import os
import dash_ag_grid as dag
# from app import app
# from app import server
# from apps import reversation, view

app.title = 'Edmonton Dashboard'
server = app.server

def load_data():
        DATA = (r"Order_table.csv")
        df=pd.read_csv(DATA,encoding='latin-1')
        return  df
df = load_data()


# embedding the navigation bar
# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
#            suppress_callback_exceptions=True)

header = dbc.Navbar(
    dbc.Container(
        [ html.Hr(),
                dbc.Row([
                
                
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                            dbc.NavbarBrand("Gilead Science", className="ms-2",style={'color': '#818589', 'fontWeight': 'bold'}),

                                dbc.NavItem(dbc.NavLink(""),style={"marginRight": "550px",'color': '#808080', 'fontWeight': 'bold'}),
                                dbc.NavItem(dbc.NavLink("Dashboard", href="#"),style={"marginRight": "55px",'color': '#808080', 'fontWeight': 'bold','fontSize': 14}),
                                dbc.NavItem(dbc.NavLink("Reserve Equipment", href="/page_2"),style={"marginRight": "55px",'color': '#818589', 'fontWeight': 'bold','fontSize': 14}),
                                dbc.NavItem(dbc.NavLink("View Reservations", href="/page_1"),style={"marginRight": "55px",'color': '#818589', 'fontWeight': 'bold','fontSize': 14}),
#                                 dbc.DropdownMenu(
#                                     [
#                                         dbc.DropdownMenuItem("Home"),
#                                         dbc.DropdownMenuItem("Some Long Item"),
#                                     ],
#                                     class_name="mr-1",
#                                     label="Menu",
#                                 ),
                            ],
                            # make sure nav takes up the full width for auto
                            # margin to get applied
                            className="create_container2 twelve columns",
#                             pills=True,
                        ),
                        id="navbar-collapse",
#                         is_open=False,
                        navbar=True,
                        
                    ),
                ],
                # the row should expand to fill the available horizontal space
                className="flex-grow-1",
            ),
        ],
        fluid=True,
    ),
    dark=False,
    color="#FFFEFA",
)

app.layout = html.Div([
    dcc.Location(id='url1', refresh=True),
    header,
    html.Div(id='page-content1')
    
])


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)



    
#*******************************************************************
df["Row ID"] = df.index
defaultColDef = { "flex": 1, "minWidth": 150, "sortable": True, "resizable": True, 
                 "filter": True}


columnD=[{"field": i,"checkboxSelection": True} 
            if i=="Row ID" else {"field": i} for i in df.columns]

newcolumnDef=[{
        "field": "Modify",
        "cellRenderer": "Button",
        "cellRendererParams": {"className": "btn btn-success"},
    }]

deleteitem={
        "field": "Modify",
        "cellRenderer": "Button",
        "cellRendererParams": {"className": "btn btn-success"},
    }
columnDefs=columnD.copy()
columnDefs.extend(newcolumnDef)


columnDefs.remove(deleteitem)
columnDefs.insert(1,deleteitem)

# print(columnDefs)


page_1_layout=html.Div([html.Div([html.Img(src="/assets/gl.jpg",style={'height':'420px','width':'100%'})]),

    html.Div([
             html.Div([
                html.Div(["Start-End DATE: ",
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=dt(1995, 8, 5),
                    max_date_allowed=dt(2017, 9, 19),
                    initial_visible_month=dt(2017, 8, 5),
                    end_date=dt(2017, 8, 25).date()
                )],
                style= {'width': '100%','text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'}), 
                html.Div(id='output-container-date-picker-range')
            ],className="pretty_container five columns",style={'height': '50px', "width": "35%",'margin':'15px'}),
    
        html.Div([html.Label("Poject Number",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                             id='target1'),
        dcc.Input(id='input1', placeholder='Insert x value', type='number', value=1,style={'display': 'inline-block','width': '55%'}),
        ], className="pretty_container four columns",style={'height': '50px', "width": "25%",'margin':'15px'}),


################################################################################   
        html.Div([html.Label("Lot Number",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                                       id='target3'),
        dcc.Input(id='input3', placeholder='Insert x value', type='number', value=1,style={'display': 'inline-block','width': '55%'}),
        ], className="pretty_container four columns",style={'height': '50px', "width": "25%",'margin':'15px'}),

#############################################################        
        html.Div([html.Label("Equipment",className='fix_label', 
            style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                                       id='target2'),
        dcc.Input(id='input2', placeholder='Insert x value', type='text', value=1,style={'display': 'inline-block','width': '71%'}),
                ], className="pretty_container four columns", style={'height': '50px', "width": "35%",'margin':'15px'}),

############################################    
        html.Div([html.Label("Reservations Status",className='fix_label', 
            style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                                       id='target4'),
        dcc.Input(id='input4', placeholder='Insert x value', type='number', value=1,style={'display': 'inline-block','width': '41%'}),
                 ], className="pretty_container four columns",style={'height': '50px', "width": "25%",'margin':'15px'}),
        
    ]),      
        
        html.Div([
        html.Button("Delete Selected", id="button"),
        html.Button("Undo", id="undo"),

        dag.AgGrid(
            id="grid",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            defaultColDef=defaultColDef,
            dashGridOptions={"rowSelection":"multiple"},
        ),
        dcc.Location(id="url", refresh=True), 
        html.Div(id='page-content'),
                  
    ],
    style={"margin": 30},
),

    
                        
    
],id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"})

@callback(
    Output("grid", "deleteSelectedRows"),
    Input("button", "n_clicks"),
    prevent_initial_call=True
)
def selected(_):
    return True

@callback(
    Output("grid", "rowData"),
    Input("undo", "n_clicks"),
    prevent_intial_call=True,
)
def undo(_):
    return df.to_dict("records")

app.clientside_callback(
    """function (n) {
        dash_ag_grid.getApi('grid').refreshInfiniteCache()
        return dash_clientside.no_update
    }""",
    Output("button", "getRowsResponse"),
    Input("button", "n-clicks"),
    prevent_initial_call=True
)

@callback(
    Output('page-content', 'children'),
    Input("grid", "cellRendererData")
)

def display_page(cellRendererData):
    # print(cellRendererData)
    if cellRendererData is None:
        # print(cellRendererData)
        return None

    if cellRendererData is not None:
        # print(cellRendererData)
        return page_3_layout
    else:
        return cellRendererData    
    
    
#************************************************************************************


page_2_layout=html.Div([
                        html.Div([html.Img(src="/assets/pic.jpg",style={'height':'420px','width':'100%'})]),
        
      html.Div([
        html.Div([html.Label("Select Equipment",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                             id='target1'),
        dcc.Dropdown(
                id='demo_dropdown',
                options=[{'label': i, 'value': i} for i in df['Order ID'].unique()
                ],
                value=[],
                multi=True,
                ),
        ], className="pretty_container four columns",style={'display': 'inline-block','height': '50px', "width": "60%",'margin':'15px'}),


################################################################################   
        html.Div([html.Label("Lot Number",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                             id='target2'),
        dcc.Dropdown(
                id='demo_dropdown1',
                options=[{'label': i, 'value': i} for i in df['Customer ID'].unique()
                ],
                value=[],
                multi=True,
                ),
        ], className="pretty_container four columns",style={'display': 'inline-block','height': '50px', "width": "60%",'margin':'15px'}),

      ]),      
        html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

                        dash_table.DataTable(
                        
                        id='table',
                         
                        tooltip ={i: {'value': i,'use_with': 'both'  # both refers to header & data cell
                        } for i in df.columns},
                        #tooltip_header={i: i for i in df.columns},
                        #style_cell={'textAlign': 'Center',
                        #            'blackSpace': 'normal','height': 'auto'},
                        #fixed_rows={'headers': True},
                        #style_as_list_view=True,
                        style_cell={
                        'blackSpace': 'normal',
                        'height': 'auto','text-align': 'left'
                        },
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        
                        page_current=0,
                        page_size=25,
                        page_action='native',
                        sort_action='native',
                        filter_action='native',
                        column_selectable="single",
                        sort_mode='multi',
                        #export_format="csv",
                        style_filter={'backgroundColor': 'white','color': 'white'},
                        style_table={'maxHeight':'400px','overflowX': 'scroll','minWidth': '100%'},
                        style_header={'backgroundColor':'#AF2103','#AF2103': 'bold','color': '#FFFEFA','fontSize': 16},
                        tooltip_delay=0,
                        tooltip_duration=None,
                        css=[{"selector": ".show-hide", "rule": "display: none"}]),
            ],className = "create_container eight columns",
                                    style={'height': '450px',"width": "100%"}),

    
                        
    
],id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"})

#**********************************************************
page_3_layout=html.Div([html.Br(),html.H1("Edit Your Record",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 18,'display': 'inline-block'},
                             id='target6'),
#                         html.Div([html.Img(src="/assets/pic.jpg",style={'height':'420px','width':'100%'})]),
        
      html.Div([
        html.Div([html.Label("Select Equipment",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                             id='target3'),
        dcc.Dropdown(
                id='demo_dropdown2',
                options=[{'label': i, 'value': i} for i in df['Order ID'].unique()
                ],
                value=[],
                multi=True,
                ),
        ], className="pretty_container four columns",style={'display': 'inline-block','height': '50px', "width": "60%",'margin':'15px'}),


################################################################################   
        html.Div([html.Label("Lot Number",className='fix_label', 
                style= {'text-align': 'left','fontWeight': 'bold','color': '#808080','fontSize': 14,'display': 'inline-block'},
                             id='target5'),
        dcc.Dropdown(
                id='demo_dropdown3',
                options=[{'label': i, 'value': i} for i in df['Customer ID'].unique()
                ],
                value=[],
                multi=True,
                ),
        ], className="pretty_container four columns",style={'display': 'inline-block','height': '50px', "width": "60%",'margin':'15px'}),

      ]),      
        html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

                        dash_table.DataTable(
                        
                        id='table2',
                         
                        tooltip ={i: {'value': i,'use_with': 'both'  # both refers to header & data cell
                        } for i in df.columns},
                        #tooltip_header={i: i for i in df.columns},
                        #style_cell={'textAlign': 'Center',
                        #            'blackSpace': 'normal','height': 'auto'},
                        #fixed_rows={'headers': True},
                        #style_as_list_view=True,
                        style_cell={
                        'blackSpace': 'normal',
                        'height': 'auto','text-align': 'left'
                        },
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        
                        page_current=0,
                        page_size=25,
                        page_action='native',
                        sort_action='native',
                        filter_action='native',
                        column_selectable="single",
                        sort_mode='multi',
                        #export_format="csv",
                        style_filter={'backgroundColor': 'white','color': 'white'},
                        style_table={'maxHeight':'400px','overflowX': 'scroll','minWidth': '100%'},
                        style_header={'backgroundColor':'#AF2103','#AF2103': 'bold','color': '#FFFEFA','fontSize': 16},
                        tooltip_delay=0,
                        tooltip_duration=None,
                        css=[{"selector": ".show-hide", "rule": "display: none"}]),
            ],className = "create_container eight columns",
                                    style={'height': '250px',"width": "100%"}),

    html.Div([
       html.Div([
                    dcc.Link(html.A('Close Page',
                           style={'color': '#ffffff', 'text-decoration': 'none'},),
                           href='/page_1'), ], className="card_inner"),
            ], className="create_container2 two columns",
                style={'textAlign': 'center', 'margin-left': '32%', 'background': '#008b8b'}),
                        
    
],id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"})

#****************************************************************************
@app.callback(Output('page-content1', 'children'),
              [Input('url1', 'pathname')])
def display_page(pathname):
    # print(pathname)
    if pathname == '/page_1':
        return page_1_layout
    elif pathname == '/page_2':
        return page_2_layout
    else:
        return dash.no_update

# if __name__ == "__main__":
#     app.run_server(debug=True)

if __name__ == '__main__':
    # cached_df = pgConn.update_cache()
    app.run_server(debug=True)


