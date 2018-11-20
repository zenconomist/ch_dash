import ch1
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, Event
import dash_table_experiments as dt
import numpy as np
import dash_graph_update as dgu
from pathlib import Path
import base64
import datetime
import io
import os


colpanel_0 = ['#646663', '#ff7433', '#23527c', '#ff7534', '#337ab7', '#fcfefb', '#6ea2ed', '#70a1ed', '#fff0eb', '#f1f6fc']
colpanel_1 = ['#2e99b0', '#fcd77f', '#ff2e4c', '#1e1548']
colpanel_2 = ['#233142', '#455d7a', '#f95959', '#facf5a']
colpanel_3 = ['#CA3542', '#276478', '#849FAD', '#AEC8C9', '#57575F'] #classic & trustworthy
colpanel_4 = ['#DA5526', '#F68930', '#FEBC38', '#D8C684', '#697F98'] #sunny & warm
colpanel_5 = ['#FAAC77', '#C9C980', '#FBEFEE', '#606B6F', '#333C3E'] #gracefully modern

colors = {
    'background': colpanel_0[0],
    'text': colpanel_5[4],
    'data1': colpanel_4[0],
    'data2': colpanel_4[2],
    'data3': colpanel_0[5],
    'data4': colpanel_0[6]
}


a = ch1.IntoPostgres("postgres server entry data") ##later referred to as "postgres server entry data"
a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)

t1 = "actual_termek" #this is the first kind of input file - the actual sold items per product. Contains invoice id, invoice line id, customer, selling price, qty, fx-rate, etc.
t2 = "actual_ugynok" #this is the second kind of input file - this contains the actual salesperson's id, and the division's names. The two division's are called 'HM' and 'KE'.
t3 = "cikkszam" #this is the 3rd kind of input file (how amazing!) and it contains mainly the product id, the products product-group category names, and the cost-prices of the products
#a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)

app = dash.Dash(__name__)

app.config['suppress_callback_exceptions']=True

app.scripts.config.serve_locally = True

##the cummul() function was written to create a cummulated value out of normal historical values
def cummul(df):
    df = df[1]
    start = df[0]
    rest = df[1:]
    list_cum_end = []
    list_cum_end.append(start)
    for i in rest:
        list_cum_end.append(list_cum_end[-1] + i)
    return list_cum_end


##the parse_contents function is the one, that does not work properly with pandas' to_excel - so in this 'light' version of the app it is not used, but I'll leave it here as comment:
#def parse_contents(contents, filename, date, file_to):
#    filename = filename[:].lower()

#    content_type, content_string = contents.split(',')
#    decoded = base64.b64decode(content_string)
#    try:
#        if '.csv' in filename:
#             Assume that the user uploaded a CSV file
#            df = pd.read_csv(
#                io.StringIO(decoded.decode('utf-8')))
#            df.to_csv(file_to / filename, sep=",", encoding='utf8')
#        elif '.xls' in filename:
#             Assume that the user uploaded an excel file
#            df = pd.read_excel(io.BytesIO(decoded))
#            xlr = pd.ExcelWriter(file_to / filename)
#            df.to_excel(xlr)
#            xlr.save()
#    except Exception as e:
#        print(e)
#        return html.Div([
#            'There was an error processing this file.'
#        ])

    #return html.Div([
#        html.H5(filename),
#        html.H6(datetime.datetime.fromtimestamp(date)),
#        html.Hr(),  # horizontal line
#    ])


##the basic app.layout contains the main tabs -> the contents of each tab is rendered later in the @app.callback() functions

app.layout = html.Div([
    html.Div([
        html.H1(['CH vállalati adatok 2018-2017'] #the company ch's corporate data for years 2018-2017
                , className="ch_base2"
                )]
             , className="ch_base"
             )
             
        ,html.Div(
    children=[

        html.Div([dcc.Tabs(id='tabs', value='kezdo', children=[
            dcc.Tab(label='Kezdőlap', value='kezdo'), #Kezdőlap = start site
            dcc.Tab(label='HM', value='HM'),
            dcc.Tab(label='KE', value='KE'),
            dcc.Tab(label='Termek', value='Termek'), #Termek = product
            #dcc.Tab(label='upload', value='upload'), #this is the upload tab, which is not used in the 'light version of the app
            ])], className='ch_tab')
        , html.Div([html.Div(id='content')] , className='ch_base'
                   )
        ],
    id='ch_dash'
   , className="ch_base"
    )]
                      ,className="ch_base"
   )

@app.callback(Output('content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'kezdo':
        return html.Div([
            html.Div([
                ##Kezdőlap oldal tartalma
                        html.Div([
                        ##row div        
                            html.Div([
                                dcc.Dropdown(id='ev',
                                             options=[
                                                 {'label': '2018', 'value': '2018'},
                                                 {'label': '2017', 'value': '2017'},
                                                 ],
                                             value=['2018','2017']
                                             ,multi=True
                                             ,clearable=False
                                             )]
                                ,className="twelve columns")

                                 ], className="row"),
                        ##Dropdown and starting page's/tab's end.
                            
                              html.Div([
                                  ##Graph-s on the starting page start here
                                  html.Div([
                            dcc.Graph(id='bevetel_evek')], className="six columns") #revenue_years
                            ,
                                       html.Div([
                            dcc.Graph(id='bevetel_evek_kum')], className="six columns") #revenue_years_cummulated
                                       ],
                                       id='kezdo', className="row")
                              ]
                     )
            ##2. row's graphs
            ,
            html.Div([
                dcc.Dropdown(id='ev_bev_fed',
                             options=[
                                 {'label': '2018', 'value': '2018'},
                                 {'label': '2017', 'value': '2017'},
                                 ],
                             value='2018'
                    
                    )
                ], className="row")
        
            ,
            html.Div([
                html.Div([
                    dcc.Graph(id='bev_fed'
                    )], className="six columns")
                ,
                html.Div([
                    dcc.Graph(id='bev_fed_kum'
                        )
                    ], className="six columns")

                ], className="row")
            
            ], id='kezdolap'
                        )
   
                    
    elif tab == 'HM':
        return html.Div([
            ##HM TAB's contents
            html.Div([
                html.Div([
                    dcc.Dropdown(id='ev_hm',
                                 options=[
                                     {'label': '2018', 'value': '2018'},
                                     {'label': '2017', 'value': '2017'},
                                     ],
                                 value=['2018','2017'],
                                 multi=True
                                 ,clearable=False
                                 )], className="twelve columns")
                    ], className="row")
            ,
            ##graphs:
            html.Div([
                html.Div([
                        dcc.Graph(id='HM_bevetelek')
                        ], className="six columns"),
                html.Div([
                    dcc.Graph(id='HM_bev_kum')
                    ], className="six columns")
                ], className="row")
            ,
            ##hm_revenue_margin
            html.Div([
                dcc.Dropdown(id='hm_bev_fed_dd',
                             options=[
                                 {'label': '2018', 'value': '2018'},
                                 {'label': '2017', 'value': '2017'},
                                 ],
                             value='2018')
                ], className="row")
            ,
            ##hm_rev_marg_graphs
            html.Div([
                html.Div([
                    dcc.Graph(id='hm_bev_fed')
                    ], className="six columns"),
                html.Div([dcc.Graph(id='hm_bev_fed_kum')
                    ], className="six columns")
                ], className="row")
            ,
            ##hm_sp_input
            html.Div([
                html.Div([
                    dcc.Dropdown(id='hm_ug_dd',
                             options=[
                                 {'label': '2018', 'value': '2018'},
                                 {'label': '2017', 'value': '2017'},
                                 ],
                             value=['2018', '2017']
                             ,multi=True
                        )
                    ], className="six columns")
                ,
                ##salesperson (sp) dropdown
                html.Div([
                    dcc.Dropdown(id='hm_ug_dd2',
                                 options=[
                                     {
                                         'label': 
                                         'KL',
                                         'value':
                                         'KL'
                                         },
                                     {##
                                         'label': 
                                         'AMGM',
                                         'value':
                                         'AMGM'
                                         },
                                         {##
                                         'label': 
                                         'GM',
                                         'value':
                                         'GM'
                                         },
                                         {##
                                         'label': 
                                         'AM',
                                         'value':
                                         'AM'
                                         },
                                         {##
                                         'label': 
                                         'Mark',
                                         'value':
                                         'Mark'
                                         },
                                         {##
                                         'label': 
                                         'HMua',
                                         'value':
                                         'HMua'
                                         },
                                         {##
                                         'label': 
                                         'KEua',
                                         'value':
                                         'KEua'
                                         },
                                         {##
                                         'label': 
                                         'KG',
                                         'value':
                                         'KG'
                                         },
                                         {##
                                         'label': 
                                         'AMGM_M',
                                         'value':
                                         'AMGM_M'
                                         },
                                         {##
                                         'label': 
                                         'SS',
                                         'value':
                                         'SS'
                                         },
                                         {##
                                         'label': 
                                         'Bel',
                                         'value':
                                         'Bel'
                                         }
                                     ]
                                 ,value='KL'

                        )
                    ], className="six columns")
                ], className="row")
            ,
            ##hm_sp_graphs
            html.Div([
                html.Div([
                    dcc.Graph(id='hm_ug'
                        )], className="six columns"),
                html.Div([
                    dcc.Graph(id='hm_ug_ho')
                    ], className="six columns")
                ], className="row")
            ])


    elif tab == 'KE':
        return html.Div([
            ##KE TAB's contents
            html.Div([
                html.Div([
                    dcc.Dropdown(id='ev_ke',
                                 options=[
                                     {'label': '2018', 'value': '2018'},
                                     {'label': '2017', 'value': '2017'},
                                     ],
                                 value=['2018','2017'],
                                 multi=True
                                 ,clearable=False
                                 )], className="twelve columns")
                    ], className="row")
            ,
            ##graphs:
            html.Div([
                html.Div([
                        dcc.Graph(id='KE_bevetelek')
                        ], className="six columns"),
                html.Div([
                    dcc.Graph(id='KE_bev_kum')
                    ], className="six columns")
                ], className="row")
                        ,
            html.Div([
                dcc.Dropdown(id='ke_bev_fed_dd',
                             options=[
                                 {'label': '2018', 'value': '2018'},
                                 {'label': '2017', 'value': '2017'},
                                 ],
                             value='2018')
                ], className="row")
            ,
            html.Div([
                html.Div([
                    dcc.Graph(id='ke_bev_fed')
                    ], className="six columns"),
                html.Div([dcc.Graph(id='ke_bev_fed_kum')
                    ], className="six columns")
                ], className="row")

            ])


    elif tab == 'Termek': #product tab
        return html.Div([
            html.Div([
            html.Div([
                dcc.Dropdown(id='termek_ev',
                             options=[
                                 {'label': '2018', 'value': '2018'},
                                 {'label': '2017', 'value': '2017'},
                                 ],
                             value='2018'
                             #,multi=True
                             #,clearable=False
                    )
                ], className="twelve columns")
            ], className="row")

            ,
            html.Div([
            html.Div([
                dcc.Graph(id='termek_bev_fed')
                ], className="six columns")
            ,
            html.Div([
                dcc.Graph(id='termek_bev')
                ], className="six columns")
            ], className="row")
           ,
            html.Div([
                html.Div([
                dcc.Dropdown(id='termek_ev_multi',
                             options=[
                                 {'label': '2018', 'value': '18'},
                                 {'label': '2017', 'value': '17'},
                                 ],
                             value=['18', '17']
                             ,multi=True
                             ,clearable=False
                    )                    
                    ])
                ], className="row")
            ,
            html.Div([
                html.Div([
                    dcc.Graph(id='termek_fh')
                    ], className="twelve columns")
                ], className="row")
            ,
            html.Div([
                html.Div([
                    dcc.Dropdown(id='tcsop',
                                 options=[
                                     {'label': 'cshm', 'value': 'cshm'},
                                     {'label': 'IEC', 'value': 'IEC'},
                                     {'label': 'kupker', 'value': 'kupker'},
                                     {'label': 'egy', 'value': 'egy'},
                                     {'label': 'cshm_cmr', 'value': 'chm_cmr'},
                                     {'label': 'felfuz', 'value': 'felfuz'},
                                     {'label': 'Homl', 'value': 'Homl'},
                                     {'label': 'delta', 'value': 'delta'},
                                     {'label': 'motofrek', 'value': 'motofrek'},
                                     {'label': 'szal', 'value': 'szal'}
                                     ],
                                 value='cshm'
                                 )
                    ], className="twelve columns")
                ],className="row")
            ,
            html.Div([
                html.Div([
                    dcc.Graph(id='tcsop_elemz')
                    ], className="six columns")
                ,
                html.Div([
                    dcc.Graph(id='tcsop_kum_elemz')
                    ], className="six columns")
                ], className="row")
            ])

##the following 'upload' tab is not used in the light version of this app, and it is not seen as well, but I leave it here

    ##upload 
    #elif tab == 'upload':
    #    return html.Div([
    #        html.Hr(),

    #        html.Hr()
    #        ,
    #        html.Div([
    #        html.Button('Feldolgoz', id='feldolgoz')], className="button")  ##this shall call the db_refresh.py 
    #        ,html.Div(id='feldolgoz_output')
    #             ,
    #             html.Div([
    #        dcc.Upload(
    #            id='upload-act_t',
    #            children=html.Div([
    #                html.Hr(),
    #                html.H6(['actual_termék']),
    #                'Húzd ide, vagy ',
    #                html.A('válaszd ki a fájlt. (.csv, .xlsx)')
    #                #,html.Footer('Kérlek, csak kisbetűs kiterjesztésű fájlt tölts fel, pl. .xlsx -et, nagybetűs kiterjesztéssel, pl. ".XLSX"-el nem működik. Köszi.')
    #                ]),
    #            style={
    #                'column_widths': '100%',
    #                'row-height': '60px',
    #                'lineHeight': '60px',
    #                'borderWidth': '1px',
    #                'borderStyle': 'dashed',
    #                'borderRadius': '5px',
    #                'textAlign': 'center',
    #                'margin': '10px'
    #                },
    #            # Allow multiple files to be uploaded
    #            multiple = True
    #            )
    #        ], className="row"),
    #        html.Div(id='output-data-act_t')

    ##,
    ##html.Button('Feltöltés', id='feltolt_gomb'
    ##    )
    #,
    #    html.Div([
    #        dcc.Upload(
    #            id='upload-act_u',
    #            children=html.Div([
    #                html.Hr(),
    #                html.H6(['actual_ügynök']),
    #                'Húzd ide, vagy ',
    #                html.A('válaszd ki a fájlt. (.csv, .xlsx)')
    #                #,html.Footer('Kérlek, csak kisbetűs kiterjesztésű fájlt tölts fel, pl. .xlsx -et, nagybetűs kiterjesztéssel, pl. ".XLSX"-el nem működik. Köszi.')
    #                ]),
    #            style={
    #                'column_widths': '100%',
    #                'row-height': '60px',
    #                'lineHeight': '60px',
    #                'borderWidth': '1px',
    #                'borderStyle': 'dashed',
    #                'borderRadius': '5px',
    #                'textAlign': 'center',
    #                'margin': '10px'
    #                },
    #            # Allow multiple files to be uploaded
    #            multiple = True
    #            )
    #        ], className="row"),
    #        html.Div(id='output-data-act_u')

    #    ,
    #    html.Div([
    #        dcc.Upload(
    #            id='upload-cikkek',
    #            children=html.Div([
    #                html.Hr(),
    #                html.H6(['cikktörzs']),
    #                'Húzd ide, vagy ',
    #                html.A('válaszd ki a fájlt. (.csv, .xlsx)')
    #                #,html.Footer('Kérlek, csak kisbetűs kiterjesztésű fájlt tölts fel, pl. .xlsx -et, nagybetűs kiterjesztéssel, pl. ".XLSX"-el nem működik. Köszi.')
    #                ]),
    #            style={
    #                'column_widths': '100%',
    #                'row-height': '60px',
    #                'lineHeight': '60px',
    #                'borderWidth': '1px',
    #                'borderStyle': 'dashed',
    #                'borderRadius': '5px',
    #                'textAlign': 'center',
    #                'margin': '10px'
    #                },
    #            # Allow multiple files to be uploaded
    #            multiple = True
    #            )
    #        ], className="row"),
    #        html.Div(id='output-data-cikkek')

    ##,
    ##html.Button('Feltöltés', id='feltolt_gomb'
    ##    )
    #], id='upload-content')


##FŐOLDAL BEVÉTELEK ÉS BEV_KUM

#####______in the following, the callbacks' main aim will be described before/inbetween the callbacks______#####

##starting page's content has 4 callbacks. 

#callback1 as Ch Havi bevételek összes = Ch firm's monthly revenues total
@app.callback(Output('bevetel_evek', 'figure')
              ,[Input('ev', 'value')])
def update_graph(input_value):
    traces_bev_evek = []
    while True:
        try:
            entry_data = ["postgres server entry data"]
            sq01 = "SELECT ho, (bevetel/1000000) as bevetel FROM ev_ho_arbev WHERE ev=" + input_value[0] + ";"        
            name1 = 'Bevétel ' + input_value[0]
            col1 = colors['data1']
            kezdo_bev1 = dgu.upd_gr_dash()
            sq02 = "SELECT ho, (bevetel/1000000) as bevetel FROM ev_ho_arbev WHERE ev=" + input_value[1] + ";"
            name2 = 'Bevétel ' + input_value[1]
            col2 = colors['data2']
            kezdo_bev2 = dgu.upd_gr_dash()
            
            traces_bev_evek = [kezdo_bev1.upd_bar(entry_data, sq01, name1, col1), kezdo_bev2.upd_bar2(entry_data, sq02, name2, col2)]
        except IndexError:
            akt_ev1 = input_value[0]
            entry_data = ["postgres server entry data"]
            sq0 = "SELECT ho, (bevetel/1000000) as bevetel FROM ev_ho_arbev WHERE ev=" + input_value[0] + ";"        
            name0 = 'Bevétel ' + input_value[0]
            col0 = colors['data1']
            kezdo_bev0 = dgu.upd_gr_dash()
            traces_bev_evek = [kezdo_bev0.upd_bar(entry_data, sq0, name0, col0)]
    
            
            
        kezdo_bev_layout = dgu.upd_gr_dash()
        title = 'Ch Havi bevételek összes'
        col_bg = colors['background']
        col_txt = colors['text']
    
        return kezdo_bev_layout.layout1(traces_bev_evek, title, 'group', col_bg, col_txt)
   


#callback2 as Ch Havi bevételek összes = Ch firm's monthly revenues total cummulated
@app.callback(Output('bevetel_evek_kum', 'figure'),
              [Input('ev', 'value')]
                  )
def update_graph_kezdo_kum(input_v_kum):
    traces_bev_evek_kum =[]
    while True:
        try:
            ed_bev_kum = ["postgres server entry data"]
            sq_bev_kum1 = "SELECT ho, (bevetel/1000000) as bevetel FROM ev_ho_arbev WHERE ev=" + input_v_kum[0] + ";"
            sq_bev_kum2 = "SELECT ho, (bevetel/1000000) as bevetel FROM ev_ho_arbev WHERE ev=" + input_v_kum[1] + ";"
            n_bev_kum1 = 'Bevétel ' + input_v_kum[0]
            n_bev_kum2 = 'Bevétel ' + input_v_kum[1]
            c1_bev_kum = colors['data1']
            c2_bev_kum = colors['data2']
            tr1_kum = dgu.upd_gr_dash()
            tr2_kum = dgu.upd_gr_dash()

            traces_bev_evek_kum = [tr1_kum.upd_gr_kum(ed_bev_kum, sq_bev_kum1, n_bev_kum1, c1_bev_kum), tr2_kum.upd_gr_kum(ed_bev_kum, sq_bev_kum2, n_bev_kum2, c2_bev_kum)]
        except IndexError:
            ed_bev_kum = ["postgres server entry data"]
            sq_bev_kum1 = "SELECT ho, (bevetel/1000000) as bevetel FROM ev_ho_arbev WHERE ev=" + input_v_kum[0] + ";"
            n_bev_kum1 = 'Bevétel ' + input_v_kum[0]
            c1_bev_kum = colors['data1']
            tr1_kum = dgu.upd_gr_dash()
            traces_bev_evek_kum = [tr1_kum.upd_gr_kum(ed_bev_kum, sq_bev_kum1, n_bev_kum1, c1_bev_kum)]

            
        t_bev_kum = 'Ch Havi bevételek kummulált'
        cb_bev_kum = colors['background']
        ct_bev_kum = colors['text']

        kezdo_bev_kum = dgu.upd_gr_dash()
        return kezdo_bev_kum.layout_kum(traces_bev_evek_kum, t_bev_kum, cb_bev_kum, ct_bev_kum)

#callback3 as Ch Havi bevétel és fedezet = Ch firm's monthly revenues and margins
@app.callback(Output('bev_fed', 'figure'),
              [Input('ev_bev_fed', 'value')])
def upd_bev_fed(akt_ev):

    trace_bev_fed = []

    ed_bev_fed = ["postgres server entry data"]
    sq1_bev_fed = "SELECT ho, sum(arbev/1000000) AS Bevétel FROM bev_fed WHERE ev=" + akt_ev + " GROUP BY ho ORDER BY ho DESC;"
    n1_bev_fed = 'Bevétel ' + akt_ev
    c1_bev_fed = colors['data1']
    bev_fed1 = dgu.upd_gr_dash()

    sq2_bev_fed = "SELECT ho, sum(arbev/1000000 - ktg/1000000) AS Fedezet FROM bev_fed WHERE ev=" + akt_ev + " GROUP BY ho ORDER BY ho DESC;"
    n2_bev_fed = 'Fedezet ' + akt_ev
    c2_bev_fed = colors['data2']
    bev_fed2 = dgu.upd_gr_dash()
    trace_bev_fed = [bev_fed1.upd_bar(ed_bev_fed, sq1_bev_fed, n1_bev_fed, c1_bev_fed), bev_fed2.upd_bar2(ed_bev_fed, sq2_bev_fed, n2_bev_fed, c2_bev_fed)]
    

    t_bev_fed = 'Ch Havi bevétel és fedezet'
    cb_bev_fed = colors['background']
    ct_bev_fed = colors['text']
    kezdo_bev = dgu.upd_gr_dash()
    return kezdo_bev.layout1(trace_bev_fed, t_bev_fed, 'group', cb_bev_fed, ct_bev_fed)

#callback4 as Ch Havi bevétel és fedezet = Ch firm's monthly revenues and margins cummulated (barchart)
@app.callback(Output('bev_fed_kum', 'figure'),
              [Input('ev_bev_fed', 'value')])
def upd_bev_fed_kum(akt_ev_kum):
    trace_bev_fed_kum = []

    ed_bev_fed_k = ["postgres server entry data"]
    sq1_bev_fed_k = "SELECT ho, sum(arbev/1000000) AS Bevétel FROM bev_fed WHERE ev=" + akt_ev_kum + " GROUP BY ho;"
    n1_bev_fed_k = 'Bevétel ' + akt_ev_kum
    c1_bev_fed_k = colors['data1']
    bev_fed1_k = dgu.upd_gr_dash()

    sq2_bev_fed_k = "SELECT ho, sum(arbev/1000000 - ktg/1000000) AS Fedezet FROM bev_fed WHERE ev=" + akt_ev_kum + " GROUP BY ho;"
    n2_bev_fed_k = 'Fedezet ' + akt_ev_kum
    c2_bev_fed_k = colors['data2']
    bev_fed2_k = dgu.upd_gr_dash()
    trace_bev_fed_kum = [bev_fed1_k.upd_bar_kum(ed_bev_fed_k, sq1_bev_fed_k, n1_bev_fed_k, c1_bev_fed_k), bev_fed2_k.upd_bar_kum(ed_bev_fed_k, sq2_bev_fed_k, n2_bev_fed_k, c2_bev_fed_k)]
    

    t_bev_fed_k = 'Ch Kummulált Havi fedezet és költség'
    cb_bev_fed_k = colors['background']
    ct_bev_fed_k = colors['text']
    kezdo_bev_k = dgu.upd_gr_dash()
    return kezdo_bev_k.layout1(trace_bev_fed_kum, t_bev_fed_k, 'group', cb_bev_fed_k, ct_bev_fed_k)
         
##HM Divisions Revenues and Margins

#callback1 HM Division's monthly revenues per year
@app.callback(Output('HM_bevetelek', 'figure'),
              [Input('ev_hm', 'value')])
def update_graph2(input_v):
    traces_hm_bev = []
    ed_hm_bev = ["postgres server entry data"]
    sq1_hm_bev = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_hm WHERE ev=" + input_v[0] + " GROUP BY ho ORDER BY ho ASC;"
    n1_hm_bev = 'Bevétel HM ' + input_v[0]
    c1_hm_bev = colpanel_0[3]
    hm_bev1 = dgu.upd_gr_dash()
    while True:
        try:
            sq2_hm_bev = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_hm WHERE ev=" + input_v[1] + " GROUP BY ho ORDER BY ho ASC;"
            n2_hm_bev = 'Bevétel HM ' + input_v[1]
            c2_hm_bev = colors['data2']            
            hm_bev2 = dgu.upd_gr_dash()            
            traces_hm_bev = [hm_bev1.upd_bar(ed_hm_bev, sq1_hm_bev, n1_hm_bev, c1_hm_bev), hm_bev2.upd_bar2(ed_hm_bev, sq2_hm_bev, n2_hm_bev, c2_hm_bev)]
        except IndexError:
            traces_hm_bev = [hm_bev1.upd_bar(ed_hm_bev, sq1_hm_bev, n1_hm_bev, c1_hm_bev)]                        
        
        t_hm_bev = 'HM üzletág havi bevételek'
        cb_hm_bev = colors['background']
        ct_hm_bev = colors['text']
        hm_bev = dgu.upd_gr_dash()
        return hm_bev.layout1(traces_hm_bev, t_hm_bev, 'group', cb_hm_bev, ct_hm_bev)


#callback2 HM Division's monthly revenues per year - cummulated
@app.callback(Output('HM_bev_kum', 'figure'),
              [Input('ev_hm', 'value')])
def upd_g_hm_k(inp_hm_k):
    traces_hm_bev_kum = []
    ed_hm_b_k = ["postgres server entry data"]
    sq_hm_b_k1 = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_hm WHERE ev=" + inp_hm_k[0] + " GROUP BY ho ORDER BY ho ASC;"
    n_hm_b_k1 = 'Bevétel HM ' + inp_hm_k[0]
    c1_hm_b_k = colors['data1']
    hm_b_k1 = dgu.upd_gr_dash()
    while True:
        try:
            sq_hm_b_k2 = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_hm WHERE ev=" + inp_hm_k[1] + " GROUP BY ho ORDER BY ho ASC;"
            n_hm_b_k2 = 'Bevétel HM ' + inp_hm_k[1]
            c2_hm_b_k = colors['data2']
            hm_b_k2 = dgu.upd_gr_dash()
            traces_hm_bev_kum = [hm_b_k1.upd_gr_kum(ed_hm_b_k, sq_hm_b_k1, n_hm_b_k1, c1_hm_b_k), hm_b_k2.upd_gr_kum(ed_hm_b_k, sq_hm_b_k2, n_hm_b_k2, c2_hm_b_k)]
        except IndexError:
            traces_hm_bev_kum = [hm_b_k1.upd_gr_kum(ed_hm_b_k, sq_hm_b_k1, n_hm_b_k1, c1_hm_b_k)]

    
        t_hm_b_k = 'HM üzletág havi bevételek kummulált'
        cb_hm_b_k = colors['background']
        ct_hm_b_k = colors['text']

        hm_b_k = dgu.upd_gr_dash()
        return hm_b_k.layout_kum(traces_hm_bev_kum, t_hm_b_k, cb_hm_b_k, ct_hm_b_k)

#callback3 HM Division's monthly revenues and margins
@app.callback(Output('hm_bev_fed', 'figure'),
              [Input('hm_bev_fed_dd', 'value')])
def upd_hm_bev_fed(hmbf_inp):
    ##hmbf = hm üzletág bev és fedezet
    trace_hmbf = []

    ed_hmbf = ["postgres server entry data"]
    sq1_hmbf = "SELECT ho, sum(arbev/1000000) AS Bevétel FROM hm_bev_fed WHERE ev=" + hmbf_inp + " GROUP BY ho ORDER BY ho DESC;"
    n1_hmbf = 'Bevétel HM ' + hmbf_inp
    c1_hmbf = colors['data1']
    hmbf1 = dgu.upd_gr_dash()

    sq2_hmbf = "SELECT ho, sum(arbev/1000000 - ktg/1000000) AS Fedezet FROM hm_bev_fed WHERE ev=" + hmbf_inp + " GROUP BY ho ORDER BY ho DESC;"
    n2_hmbf = 'Fedezet HM' + hmbf_inp
    c2_hmbf = colors['data2']
    hmbf2 = dgu.upd_gr_dash()
    trace_hmbf = [hmbf1.upd_bar(ed_hmbf, sq1_hmbf, n1_hmbf, c1_hmbf), hmbf2.upd_bar2(ed_hmbf, sq2_hmbf, n2_hmbf, c2_hmbf)]
    

    t_hmbf = 'Ch Havi bevétel és fedezet'
    cb_hmbf = colors['background']
    ct_hmbf = colors['text']
    hmbf = dgu.upd_gr_dash()
    return hmbf.layout1(trace_hmbf, t_hmbf, 'group', cb_hmbf, ct_hmbf)

#callback4 HM Division's monthly revenues and margins - cummulated
@app.callback(Output('hm_bev_fed_kum', 'figure'),
              [Input('hm_bev_fed_dd', 'value')])
def upd_hm_bev_fed_kum(hmbfk_inp):
    trace_hmbf_kum = []

    ed_hmbf_k = ["postgres server entry data"]
    sq1_hmbf_k = "SELECT ho, sum(arbev/1000000) AS Bevétel FROM hm_bev_fed WHERE ev=" + hmbfk_inp + " GROUP BY ho;"
    n1_hmbf_k = 'Költség ' + hmbfk_inp
    c1_hmbf_k = colors['data1']
    hmbf1_k = dgu.upd_gr_dash()

    sq2_hmbf_k = "SELECT ho, sum(arbev/1000000 - ktg/1000000) AS Fedezet FROM hm_bev_fed WHERE ev=" + hmbfk_inp + " GROUP BY ho;"
    n2_hmbf_k = 'Fedezet ' + hmbfk_inp
    c2_hmbf_k = colors['data2']
    hmbf2_k = dgu.upd_gr_dash()
    trace_hmbf_kum = [hmbf1_k.upd_bar_kum(ed_hmbf_k, sq1_hmbf_k, n1_hmbf_k, c1_hmbf_k), hmbf2_k.upd_bar_kum(ed_hmbf_k, sq2_hmbf_k, n2_hmbf_k, c2_hmbf_k)]
    

    t_hmbf_k = 'Ch Kummulált Havi fedezet és költség'
    cb_hmbf_k = colors['background']
    ct_hmbf_k = colors['text']
    hmbf_k = dgu.upd_gr_dash()
    return hmbf_k.layout1(trace_hmbf_kum, t_hmbf_k, 'group', cb_hmbf_k, ct_hmbf_k)

#callback5 HM Division's revenue per year per salesperson
@app.callback(Output('hm_ug', 'figure'),
              [Input('hm_ug_dd', 'value')])
def upd_hm_ug(hmug_ev):
    tr_hmug = []
    while True:
        try:
            ##ez most még nem jó, mert a fedezeti adatokat nem hozza!
            ed_hmug = ["postgres server entry data"]
            sq1_hmug = "SELECT ug_rov, sum(arbev/1000) as arbev, sum(arbev-ktg)/1000 as fed FROM hm_ev_ua_ho_ug WHERE ev=" + hmug_ev[0] + " GROUP BY ug_rov ORDER BY arbev ASC;"        
            n1_hmug = 'Bevétel ' + hmug_ev[0]
            c1_hmug = colors['data1']
            hmug1 = dgu.upd_gr_dash()
            sq2_hmug = "SELECT ug_rov, sum(arbev)/1000 as arbev, sum(arbev-ktg)/1000 as fed FROM hm_ev_ua_ho_ug WHERE ev=" + hmug_ev[1] + " GROUP BY ug_rov ORDER BY arbev ASC;"
            n2_hmug = 'Bevétel ' + hmug_ev[1]
            c2_hmug = colors['data2']
            hmug2 = dgu.upd_gr_dash()
            
            tr_hmug = [hmug1.upd_bar_n(ed_hmug, sq1_hmug, n1_hmug, c1_hmug), hmug2.upd_bar_n2(ed_hmug, sq2_hmug, n2_hmug, c2_hmug)]
        except IndexError:
            ed_hmug = ["postgres server entry data"]
            sq0_hmug = "SELECT ug_rov, sum(arbev)/1000 as arbev, sum(arbev-ktg)/1000 as fed FROM hm_ev_ua_ho_ug WHERE ev=" + hmug_ev[0] + " GROUP BY ug_rov ORDER BY arbev ASC;"        
            n0_hmug = 'Bevétel ' + hmug_ev[0]
            c0_hmug = colors['data1']
            hmug0 = dgu.upd_gr_dash()
            tr_hmug = [hmug0.upd_bar_n(ed_hmug, sq0_hmug, n0_hmug, c0_hmug)]
    
            
            
        hmug_lo = dgu.upd_gr_dash()
        t_hmug = 'Ch Havi bevételek összes'
        cb_hmug = colors['background']
        ct_hmug = colors['text']
    
        return hmug_lo.layout_n(tr_hmug, t_hmug, 'group', cb_hmug, ct_hmug)

#callback6 HM Division's revenue per month per year per salesperson
@app.callback(Output('hm_ug_ho', 'figure'),
              [Input('hm_ug_dd2', 'value'),
               Input('hm_ug_dd', 'value')]
              )
def upd_hm_ug_ho(ugynok, ev):
    tr_hmug_ho = []
    while True:
        try:
            ed_hmug_ho = ["postgres server entry data"]
            sq1_hmug_ho = "SELECT ho, sum(arbev/1000) as arbev, sum(arbev-ktg)/1000 as fed FROM hm_ev_ua_ho_ug WHERE ug_rov='" + ugynok + "' AND ev=" + ev[0] + " GROUP BY ho;"        
            n1_hmug_ho = 'Bevétel ' + ugynok + ' ' + ev[0]
            c1_hmug_ho = colors['data1']
            hmug_ho1 = dgu.upd_gr_dash()
            sq2_hmug_ho = "SELECT ho, sum(arbev)/1000 as arbev, sum(arbev-ktg)/1000 as fed FROM hm_ev_ua_ho_ug WHERE ug_rov='" + ugynok + "' AND ev=" + ev[1] + " GROUP BY ho;"
            n2_hmug_ho = 'Bevétel ' + ugynok + ' ' + ev[1]
            c2_hmug_ho = colors['data2']
            hmug_ho2 = dgu.upd_gr_dash()
            
            tr_hmug_ho = [hmug_ho1.upd_bar(ed_hmug_ho, sq1_hmug_ho, n1_hmug_ho, c1_hmug_ho), hmug_ho2.upd_bar(ed_hmug_ho, sq2_hmug_ho, n2_hmug_ho, c2_hmug_ho)]
        except IndexError:
            ed_hmug_ho = ["postgres server entry data"]
            sq0_hmug_ho = "SELECT ho, sum(arbev)/1000 as arbev, sum(arbev-ktg)/1000 as fed FROM hm_ev_ua_ho_ug WHERE ug_rov='" + ugynok + "' AND ev=" + ev[0] + " GROUP BY ho;"        
            n0_hmug_ho = 'Bevétel ' + ugynok + ' ' + ev[0]
            c0_hmug_ho = colors['data1']
            hmug_ho0 = dgu.upd_gr_dash()
            tr_hmug_ho = [hmug_ho0.upd_bar(ed_hmug_ho, sq0_hmug_ho, n0_hmug_ho, c0_hmug_ho)]
    
            
            
        hmug_ho_lo = dgu.upd_gr_dash()
        t_hmug_ho = 'Ch Havi bevételek ügynök/év'
        cb_hmug_ho = colors['background']
        ct_hmug_ho = colors['text']
    
        return hmug_ho_lo.layout2(tr_hmug_ho, t_hmug_ho, 'group', cb_hmug_ho, ct_hmug_ho)

##KE BEV és BEV_KUM

#callback1 KE Division's monthly revenues per year
@app.callback(Output('KE_bevetelek', 'figure'),
              [Input('ev_ke', 'value')])
def update_graph2(input_v_ke):
    traces_ke_bev = []
    ed_ke_bev = ["postgres server entry data"]
    sq1_ke_bev = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_ke WHERE ev=" + input_v_ke[0] + " GROUP BY ho ORDER BY ho ASC;"
    n1_ke_bev = 'Bevétel KE' + input_v_ke[0]
    c1_ke_bev = colpanel_0[3]
    ke_bev1 = dgu.upd_gr_dash()
    while True:
        try:
            sq2_ke_bev = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_ke WHERE ev=" + input_v_ke[1] + " GROUP BY ho ORDER BY ho ASC;"
            n2_ke_bev = 'Bevétel KE' + input_v_ke[1]
            c2_ke_bev = colors['data2']
            ke_bev2 = dgu.upd_gr_dash()
            traces_ke_bev = [ke_bev1.upd_bar(ed_ke_bev, sq1_ke_bev, n1_ke_bev, c1_ke_bev), ke_bev2.upd_bar(ed_ke_bev, sq2_ke_bev, n2_ke_bev, c2_ke_bev)]
        except IndexError:
            traces_ke_bev = [ke_bev1.upd_bar(ed_ke_bev, sq1_ke_bev, n1_ke_bev, c1_ke_bev)]

    
            
        t_ke_bev = 'KE üzletág havi bevételek'
        cb_ke_bev = colors['background']
        ct_ke_bev = colors['text']
        ke_bev = dgu.upd_gr_dash()
        return ke_bev.layout1(traces_ke_bev, t_ke_bev, 'group', cb_ke_bev, ct_ke_bev)


#callback2 KE Division's monthly revenues per year - cummulated
@app.callback(Output('KE_bev_kum', 'figure'),
              [Input('ev_ke', 'value')])
def upd_g_hm_k(inp_ke_k):
    traces_ke_bev_kum = []
    ed_ke_b_k = ["postgres server entry data"]
    sq_ke_b_k1 = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_ke WHERE ev=" + inp_ke_k[0] + " GROUP BY ho ORDER BY ho ASC;"
    n_ke_b_k1 = 'Bevétel KE ' + inp_ke_k[0]
    c1_ke_b_k = colors['data1']
    ke_b_k1 = dgu.upd_gr_dash()
    while True:
        try:
            sq_ke_b_k2 = "SELECT ho, sum(arbev)/1000000 as Bevetel FROM uzletagi_bev_ke WHERE ev=" + inp_ke_k[1] + " GROUP BY ho ORDER BY ho ASC;"
            n_ke_b_k2 = 'Bevétel KE ' + inp_ke_k[1]
            c2_ke_b_k = colors['data2']
            ke_b_k2 = dgu.upd_gr_dash()
            traces_ke_bev_kum = [ke_b_k1.upd_gr_kum(ed_ke_b_k, sq_ke_b_k1, n_ke_b_k1, c1_ke_b_k), ke_b_k2.upd_gr_kum(ed_ke_b_k, sq_ke_b_k2, n_ke_b_k2, c2_ke_b_k)]
        except IndexError:
            traces_ke_bev_kum = [ke_b_k1.upd_gr_kum(ed_ke_b_k, sq_ke_b_k1, n_ke_b_k1, c1_ke_b_k)]
    
        cb_ke_b_k = colors['background']
        ct_ke_b_k = colors['text']
        t_ke_b_k = 'ke üzletág havi bevételek kummulált'

        ke_b_k = dgu.upd_gr_dash()
        return ke_b_k.layout_kum(traces_ke_bev_kum, t_ke_b_k, cb_ke_b_k, ct_ke_b_k)


#callback3 KE Division's monthly revenues and margins
@app.callback(Output('ke_bev_fed', 'figure'),
              [Input('ke_bev_fed_dd', 'value')])
def upd_ke_bev_fed(kebf_inp):
    ##kebf = ke üzletág bev és fedezet
    trace_kebf = []

    ed_kebf = ["postgres server entry data"]
    sq1_kebf = "SELECT ho, sum(arbev/1000000) AS Bevétel FROM ke_bev_fed WHERE ev=" + kebf_inp + " GROUP BY ho ORDER BY ho DESC;"
    n1_kebf = 'Bevétel ke ' + kebf_inp
    c1_kebf = colors['data1']
    kebf1 = dgu.upd_gr_dash()

    sq2_kebf = "SELECT ho, sum(arbev/1000000 - ktg/1000000) AS Fedezet FROM ke_bev_fed WHERE ev=" + kebf_inp + " GROUP BY ho ORDER BY ho DESC;"
    n2_kebf = 'Fedezet ke' + kebf_inp
    c2_kebf = colors['data2']
    kebf2 = dgu.upd_gr_dash()
    trace_kebf = [kebf1.upd_bar(ed_kebf, sq1_kebf, n1_kebf, c1_kebf), kebf2.upd_bar(ed_kebf, sq2_kebf, n2_kebf, c2_kebf)]

    t_kebf = 'Ch Havi bevétel és fedezet'
    cb_kebf = colors['background']
    ct_kebf = colors['text']
    kebf = dgu.upd_gr_dash()
    return kebf.layout1(trace_kebf, t_kebf, 'group', cb_kebf, ct_kebf)

#callback4 KE Division's monthly revenues and margins - cummulated
@app.callback(Output('ke_bev_fed_kum', 'figure'),
              [Input('ke_bev_fed_dd', 'value')])
def upd_ke_bev_fed_kum(kebfk_inp):
    trace_kebf_kum = []

    ed_kebf_k = ["postgres server entry data"]
    sq1_kebf_k = "SELECT ho, sum(arbev/1000000) AS Bevétel FROM ke_bev_fed WHERE ev=" + kebfk_inp + " GROUP BY ho;"
    n1_kebf_k = 'Költség ' + kebfk_inp
    c1_kebf_k = colors['data1']
    kebf1_k = dgu.upd_gr_dash()

    sq2_kebf_k = "SELECT ho, sum(arbev/1000000 - ktg/1000000) AS Fedezet FROM ke_bev_fed WHERE ev=" + kebfk_inp + " GROUP BY ho;"
    n2_kebf_k = 'Fedezet ' + kebfk_inp
    c2_kebf_k = colors['data2']
    kebf2_k = dgu.upd_gr_dash()
    trace_kebf_kum = [kebf1_k.upd_bar_kum(ed_kebf_k, sq1_kebf_k, n1_kebf_k, c1_kebf_k), kebf2_k.upd_bar_kum(ed_kebf_k, sq2_kebf_k, n2_kebf_k, c2_kebf_k)]
    

    t_kebf_k = 'Ch Kummulált Havi fedezet és költség'
    cb_kebf_k = colors['background']
    ct_kebf_k = colors['text']
    kebf_k = dgu.upd_gr_dash()
    return kebf_k.layout1(trace_kebf_kum, t_kebf_k, 'group', cb_kebf_k, ct_kebf_k)


##Product

#callback1 Margins, costs and margin percentage per productgroup per year
@app.callback(Output('termek_bev_fed', 'figure'),
              [Input('termek_ev', 'value')])
def upd_termek_bev_fed(tbf_ev):
    ##termekbf = termékcsoportok bev és fedezet
    trace_termekbf = []
    tbf_ua = 'Hajtómű'

    ed_termekbf = ["postgres server entry data"]

    sq1_termekbf = "SELECT tcs_rov, SUM(ktg) AS ktsg FROM tcsop_hm_18 GROUP BY tcs_rov ORDER BY ktsg DESC;"
    n1_termekbf = 'Költség ' + tbf_ua + ' ' + tbf_ev
    c1_termekbf = colors['data1']
    termekbf1 = dgu.upd_gr_dash()

    sq2_termekbf = "SELECT tcs_rov, SUM(bev-ktg) AS fed FROM tcsop_hm_18 GROUP BY tcs_rov;"
    n2_termekbf = 'Fedezet ' + tbf_ua + ' ' + tbf_ev
    c2_termekbf = colors['data2']
    termekbf2 = dgu.upd_gr_dash()
    
    sq3_termekbf = "SELECT tcs_rov, SUM((bev-ktg)/bev)*100 AS fh FROM tcsop_hm_18 GROUP BY tcs_rov ORDER BY fh DESC;"
    n3_termekbf = 'Fedezeti hányad ' + tbf_ua + ' ' + tbf_ev
    c3_termekbf = colors['data3']
    termekbf3 = dgu.upd_gr_dash()
    
    trace_termekbf = [termekbf1.upd_bar_t(ed_termekbf, sq1_termekbf, n1_termekbf, c1_termekbf), termekbf2.upd_bar_t2(ed_termekbf, sq2_termekbf, n2_termekbf, c2_termekbf), termekbf3.upd_scatter_t(ed_termekbf,sq3_termekbf, n3_termekbf, c3_termekbf)]


    t_termekbf = 'Ch bevétel és fedezet termékcsoportonként'
    cb_termekbf = colors['background']
    ct_termekbf = colors['text']
    termekbf = dgu.upd_gr_dash()
    return termekbf.layout_t(trace_termekbf, t_termekbf, 'stack', cb_termekbf, ct_termekbf)


#callback2 Revenues and margin percentage per productgroup per year
@app.callback(Output('termek_bev', 'figure'),
              [Input('termek_ev', 'value')])
def upd_termek_bev(tb_ev):
    ##termek_bv = termékcsoportok bev
    trace_termek_bev = []
    tbf_ua = 'HM'

    ed_termek_bev = ["postgres server entry data"]

    sq0_termek_bev = "SELECT tcs_rov, SUM(bev) AS arbev FROM tcsop_hm_18 GROUP BY tcs_rov ORDER BY arbev DESC;"
    n0_termek_bev = 'Bevétel ' + tbf_ua + ' ' + tb_ev
    c0_termek_bev = colors['data4']
    termek_bev0 = dgu.upd_gr_dash()

    sq1_termek_bev = "SELECT tcs_rov, SUM((bev-ktg)/bev)*100 AS fh FROM tcsop_hm_18 GROUP BY tcs_rov;"
    n1_termek_bev = 'Fedezeti hányad ' + tbf_ua + ' ' + tb_ev
    c1_termek_bev = colors['data3']
    termek_bev1 = dgu.upd_gr_dash()


    trace_termek_bev = [termek_bev0.upd_bar_t(ed_termek_bev, sq0_termek_bev, n0_termek_bev, c0_termek_bev), termek_bev1.upd_scatter_t(ed_termek_bev, sq1_termek_bev, n1_termek_bev, c1_termek_bev)]

    t_termek_bev = 'Ch bevétel és termékcsoportonként'
    cb_termek_bev = colors['background']
    ct_termek_bev = colors['text']
    termek_bev = dgu.upd_gr_dash()
    
    return termek_bev.layout_t(trace_termek_bev, t_termek_bev, 'group', cb_termek_bev, ct_termek_bev)


#callback3 margin percentage per year per productgroup
@app.callback(Output('termek_fh', 'figure'),
              [Input('termek_ev_multi', 'value')])
def upd_termek_bev(tfh_ev):
    ##termek_fh = termékcsoportok fedezeti hányada
    trace_termek_bev = []
    tfh_ua = 'HM'

    ed_tfh = ["postgres server entry data"]

    sq0_tfh = "SELECT tcs_rov, SUM((bev-ktg)/bev)*100 AS fh FROM tcsop_hm_" + tfh_ev[0] + " GROUP BY tcs_rov ORDER BY fh DESC;"
    n0_tfh = 'Fedezeti hányad ' + tfh_ua + ' ' + tfh_ev[0]
    c0_tfh = colors['data1']
    tfh0 = dgu.upd_gr_dash()
    while True:
        try:
            sq1_tfh = "SELECT tcs_rov, SUM((bev-ktg)/bev)*100 AS fh FROM tcsop_hm_" + tfh_ev[1] + " GROUP BY tcs_rov;"
            n1_tfh = 'Fedezeti hányad ' + tfh_ua + ' ' + tfh_ev[1]
            c1_tfh = colors['data2']
            tfh1 = dgu.upd_gr_dash()
            
            trace_tfh = [tfh0.upd_scatter_t(ed_tfh, sq0_tfh, n0_tfh, c0_tfh), tfh1.upd_scatter_t(ed_tfh, sq1_tfh, n1_tfh, c1_tfh)]
        except IndexError:
            trace_tfh = [tfh0.upd_scatter_t(ed_tfh, sq0_tfh, n0_tfh, c0_tfh)]


        t_tfh = 'Ch fedezetek termékcsoportonként'
        cb_tfh = colors['data4']
        ct_tfh = colors['text']
        tfh = dgu.upd_gr_dash()
    
        return tfh.layout_custom_1(trace_tfh, t_tfh, cb_tfh, ct_tfh, 60, 60, 100, 120)

#callback4 margins, costs, margin percentage per product group per month per 2018
@app.callback(Output('tcsop_elemz', 'figure'),
              [Input('tcsop', 'value')])
def upd_termek_bev_fed(tcsop):
    ##termekbf = termékcsoportok bev és fedezet
    trace_tcsopbf = []
    tbf_ua = 'Hajtómű'

    ed_tcsopbf = ["postgres server entry data"]

    sq1_tcsopbf = "SELECT ho, SUM(ktg)/1000000 AS ktsg FROM hm_tcsop_ho_18 WHERE tcs_rov='" + tcsop + "' GROUP BY ho ORDER BY ho;"
    n1_tcsopbf = 'Költség '+ tcsop
    c1_tcsopbf = colors['data1']
    tcsopbf1 = dgu.upd_gr_dash()

    sq2_tcsopbf = "SELECT ho, SUM(bev-ktg)/1000000 AS fed FROM hm_tcsop_ho_18 WHERE tcs_rov='" + tcsop + "' GROUP BY ho ORDER BY ho;"
    n2_tcsopbf = 'Fedezet '+ tcsop
    c2_tcsopbf = colors['data2']
    tcsopbf2 = dgu.upd_gr_dash()
    
    sq3_tcsopbf = "SELECT ho, SUM((bev-ktg)/bev)*100 AS fh FROM hm_tcsop_ho_18 WHERE tcs_rov='" + tcsop + "' GROUP BY ho ORDER BY ho;"
    n3_tcsopbf = 'Fh% '+ tcsop
    c3_tcsopbf = colors['data3']
    tcsopbf3 = dgu.upd_gr_dash()
    
    trace_tcsopbf = [tcsopbf1.upd_bar_t(ed_tcsopbf, sq1_tcsopbf, n1_tcsopbf, c1_tcsopbf), tcsopbf2.upd_bar_t2(ed_tcsopbf, sq2_tcsopbf, n2_tcsopbf, c2_tcsopbf), tcsopbf3.upd_scatter_t(ed_tcsopbf,sq3_tcsopbf, n3_tcsopbf, c3_tcsopbf)]


    t_tcsopbf = 'Ch bevétel és fedezet termékcsoportonként'
    cb_tcsopbf = colors['background']
    ct_tcsopbf = colors['text']
    tcsopbf = dgu.upd_gr_dash()
    return tcsopbf.layout1(trace_tcsopbf, t_tcsopbf, 'stack', cb_tcsopbf, ct_tcsopbf)


#callback5 margins, costs, margin percentage per product group per month per 2018 - cummulated
@app.callback(Output('tcsop_kum_elemz', 'figure'),
              [Input('tcsop', 'value')])
def upd_termek_bev_fed(tck):
    ##termekbf = termékcsoportok bev és fedezet
    trace_tcbf_kum = []
    tbf_ua = 'Hajtómű'

    ed_tcbf_kum = ["postgres server entry data"]

    sq1_tcbf_kum = "SELECT ho, SUM(ktg)/1000000 AS ktsg FROM hm_tcsop_ho_18 WHERE tcs_rov='" + tck + "' GROUP BY ho ORDER BY ho;"
    n1_tcbf_kum = 'Költség '+ tck
    c1_tcbf_kum = colors['data1']
    tcbf_kum1 = dgu.upd_gr_dash()

    sq2_tcbf_kum = "SELECT ho, SUM(bev-ktg)/1000000 AS fed FROM hm_tcsop_ho_18 WHERE tcs_rov='" + tck + "' GROUP BY ho ORDER BY ho;"
    n2_tcbf_kum = 'Fedezet ' + tck
    c2_tcbf_kum = colors['data2']
    tcbf_kum2 = dgu.upd_gr_dash()
    
    sq3_tcbf_kum = "SELECT ho, SUM((bev-ktg)/bev)*100 AS fh FROM hm_tcsop_ho_18 WHERE tcs_rov='" + tck + "' GROUP BY ho ORDER BY ho;"
    n3_tcbf_kum = 'Fh% '+ tck
    c3_tcbf_kum = colors['data3']
    tcbf_kum3 = dgu.upd_gr_dash()
    
    trace_tcbf_kum = [tcbf_kum1.upd_bar_kum(ed_tcbf_kum, sq1_tcbf_kum, n1_tcbf_kum, c1_tcbf_kum), tcbf_kum2.upd_bar_kum(ed_tcbf_kum, sq2_tcbf_kum, n2_tcbf_kum, c2_tcbf_kum), tcbf_kum3.upd_scatter_t(ed_tcbf_kum,sq3_tcbf_kum, n3_tcbf_kum, c3_tcbf_kum)]


    t_tcbf_kum = 'Ch bevétel és fedezet termékcsoportonként'
    cb_tcbf_kum = colors['background']
    ct_tcbf_kum = colors['text']
    tcbf_kum = dgu.upd_gr_dash()
    return tcbf_kum.layout1(trace_tcbf_kum, t_tcbf_kum, 'stack', cb_tcbf_kum, ct_tcbf_kum)



server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
