import pandas as pd
import numpy as np
import dash
import flask
import math
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

pokemon=pd.read_csv('pokedex_basic.csv')
pokemon['Type']=pokemon.Type.apply(lambda x: x.lower())

p_types=pd.DataFrame(['rock','grass','fighting','dark','flying','ice','water','fire','ground','steel','fairy','normal',
         'bug','poison','psychic','ghost','electric','dragon'],columns=['Type']).set_index('Type').T


app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.layout=html.Div(children=[
    html.H1('Pokemon Search Tool',style={'textAlign': 'center','fontSize':30}),
    html.H2('Select some attributes and see which Pokemon match them!',style={'textAlign': 'center','fontSize':30} ),
    html.Div(children=[
        html.H2('Choose Attributes'),
        dcc.Dropdown(id='options',
            options=[
                {'label': 'Type', 'value': 'type'},
                {'label': 'Name', 'value': 'name'},
                {'label': 'Total', 'value': 'total'},
                {'label': 'Attack', 'value': 'attacks'},
                {'label': 'Defense', 'value': 'defenses'},
                {'label': 'HP', 'value': 'hp'},
                {'label': 'Special Attack', 'value': 'spattack'},
                {'label': 'Special Defense', 'value': 'spdefense'},
                {'label': 'Speed', 'value': 'speed'}
            ],
            multi=True,
            searchable=False
        ),
        html.Div(children=[
            html.Div(id='name',children=[
                html.H2('Type the name of the Pokemon'),
                dcc.Dropdown(id='nm',
                             options=[{'label':i,'value':i} for i in pokemon.Name],
                             multi=False,
                             searchable=True
                )
                
            ],
            style={'display':'none'}
            ),
            html.Div(id='type',children=[
                html.H2('Select Pokemon type.'),
                dcc.Dropdown(id='type1',
                    options=[{'label':i.upper(),'value':i} for i in p_types]
                ),
                html.H3('Second Type?',
                        
                ),
                dcc.RadioItems(id='2nd type',
                               options=[
                                   {'label':'Yes','value':'yes'},
                                   {'label':'No','value':'no'}
                               ],
                               value='no',
                               
                           
                ),
                dcc.Dropdown(id='type2',
                    style={'display':'none'}
                )
            ],
            style={'display':'none'}
            ),
            html.Div(id='total',children=[
                     html.H2('Total of all Attributes'),
                     dcc.Dropdown(id='highlowtotal',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='totalinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'},
                             
                     )
            ],
            style={'display':'none'}
            ),
            html.Div(id='attack',children=[
                     html.H2('Attack Stat'),
                     dcc.Dropdown(id='highlowattack',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='attackinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'}
                     )
            ],
            style={'display':'none'}
            ),
            html.Div(id='defense',children=[
                     html.H2('Defense Stat'),
                     dcc.Dropdown(id='highlowdefense',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='defenseinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'}
                     )
            ],
            style={'display':'none'}
            ),
            html.Div(id='hp',children=[
                     html.H2('Health Points'),
                     dcc.Dropdown(id='highlowhp',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='hpinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'}
                     )
            ],
            style={'display':'none'}
            ),
            html.Div(id='speed',children=[
                     html.H2('Speed'),
                     dcc.Dropdown(id='highlowspeed',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='speedinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'}
                     )
            ],
            style={'display':'none'}
            ),
            html.Div(id='spattack',children=[
                     html.H2('Special Attack Stat'),
                     dcc.Dropdown(id='highlowspattack',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='spattackinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'}
                     )
            ],
            style={'display':'none'}
            ),
            html.Div(id='spdefense',children=[
                     html.H2('Special Defense Stat'),
                     dcc.Dropdown(id='highlowspdefense',
                                  options=[
                                      {'label':'Greater than or equal to','value':0},
                                      {'label':'Less than or equal to','value':1}
                                  ],
                                  searchable=False
                     ),
                     dcc.Input(id='spdefenseinput',
                               placeholder='Enter Value',
                               inputMode='number',
                               type='number',
                               style={'font-size':'20px','height':'30px'}
                     )
            ],
            style={'display':'none'}
            )
        ]
        
        ),
        html.Br(),
        html.Div(id='output',
                 style={'display':'none'}
        )
        
    ],style={'textAlign': 'center',
                   'fontSize':20} )
    
],style={'backgroundColor':'red'})
@app.callback([Output('type2','style'),
               Output('type2','options')],
              [Input('type1','value'),
               Input('2nd type','value')])
def type_two(type1,option):
    if option=='yes':
        p_type=p_types.drop(type1,axis=1)
        options=[{'label':i.upper(),'value':i} for i in p_type.columns]
        return {'display':True},options
    else:
        return {'display':'none'},[]
@app.callback(Output('name','style'),
             [Input('options','value')])
def name_reveal(value):
    if 'name' in value:
        return {'display':True}
    else:
        return {'display':'none'}     
@app.callback(Output('type','style'),
             [Input('options','value')])
def type_reveal(value):
    if 'type' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('total','style'),
             [Input('options','value')])
def total_reveal(value):
    if 'total' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('attack','style'),
             [Input('options','value')])
def attack_reveal(value):
    if 'attacks' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('defense','style'),
             [Input('options','value')])
def defense_reveal(value):
    if 'defenses' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('hp','style'),
             [Input('options','value')])
def hp_reveal(value):
    if 'hp' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('speed','style'),
             [Input('options','value')])
def speed_reveal(value):
    if 'speed' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('spattack','style'),
             [Input('options','value')])
def spattack_reveal(value):
    if 'spattack' in value:
        return {'display':True}
    else:
        return {'display':'none'}
@app.callback(Output('spdefense','style'),
             [Input('options','value')])
def spdefense_reveal(value):
    if 'spdefense' in value:
        return {'display':True}
    else:
        return {'display':'none'}        
@app.callback([Output('output','style'),
               Output('output','children')],
              [Input('options','value'),
               Input('type1','value'),
               Input('nm','value'),
               Input('2nd type','value'),
               Input('type2','value'),
               Input('highlowtotal','value'),
               Input('totalinput','value'),
               Input('highlowattack','value'),
               Input('attackinput','value'),
               Input('highlowdefense','value'),
               Input('defenseinput','value'),
               Input('highlowhp','value'),
               Input('hpinput','value'),
               Input('highlowspeed','value'),
               Input('speedinput','value'),
               Input('highlowspattack','value'),
               Input('spattackinput','value'),
               Input('highlowspdefense','value'),
               Input('spdefenseinput','value'),
               ])
def output(options,type1,name,typo,type2,hltotal,total,hlattack,attack,hldefense,defense,hlhp,hp,hlspeed,speed,hlspattack,spattack,hlspdefense,spdefense):
    pokemon=pd.read_csv('pokedex_basic.csv')
    if 'name' in options:
        name_df=pd.DataFrame(columns=[col for col in pokemon.columns])
        for i in range(len(pokemon)):
            if name in pokemon.Name[i]:
                ndf=pd.DataFrame(pokemon.iloc[i],columns=[i]).T
                name_df=pd.concat([name_df,ndf])
        pokemon=pd.merge(pokemon,name_df)
    if 'type' in options:
        first=type1[0].upper()+type1[1:]
        if typo=='no':
            type_df=pd.DataFrame(columns=[col for col in pokemon.columns])
            for i in range(len(pokemon)):
                if first in pokemon.Type[i]:
                    tdf=pd.DataFrame(pokemon.iloc[i],columns=[i]).T
                    type_df=pd.concat([type_df,tdf])
        elif typo=='yes':
            second=type2[0].upper()+type2[1:]
            t1=first+second
            t2=second+first
            type_df=pokemon[(pokemon.Type==t1)|(pokemon.Type==t2)]
        pokemon=pd.merge(pokemon,type_df)
    if 'total' in options:
        if hltotal==0:
            total_df=pokemon[pokemon.Total>=total]
        else:
            total_df=pokemon[pokemon.Total<=total]
        pokemon=pd.merge(pokemon,total_df)
    if 'attacks' in options:
        if hlattack==0:
            attack_df=pokemon[pokemon.Attack>=attack]
        else:
            attack_df=pokemon[pokemon.Attack<=attack]
        pokemon=pd.merge(pokemon,attack_df)
    if 'defenses' in options:
        if hldefense==0:
            defense_df=pokemon[pokemon.Defense>=defense]
        else:
            defense_df=pokemon[pokemon.Defense<=defense]
        pokemon=pd.merge(pokemon,defense_df)
    if 'hp' in options:
        if hlhp==0:
            hp_df=pokemon[pokemon.HP>=hp]
        else:
            hp_df=pokemon[pokemon.HP<=hp]
        pokemon=pd.merge(pokemon,hp_df)
    if 'speed' in options:
        if hlspeed==0:
            speed_df=pokemon[pokemon.Speed>=speed]
        else:
            speed_df=pokemon[pokemon.Speed<=speed]
        pokemon=pd.merge(pokemon,speed_df)
    if 'spattack' in options:
        if hlspattack==0:
            spattack_df=pokemon[pokemon.SpecialAttack>=spattack]
        else:
            spattack_df=pokemon[pokemon.SpecialAttack<=spattack]
        pokemon=pd.merge(pokemon,spattack_df)
    if 'spdefense' in options:
        if hlspdefense==0:
            spdefense_df=pokemon[pokemon.SpecialDefense>=spdefense]
        else:
            spdefense_df=pokemon[pokemon.SpecialDefense<=spdefense]
        pokemon=pd.merge(pokemon,spdefense_df)
    children=[dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in pokemon.columns],
                                            data=pokemon.to_dict('records'),
                                            sort_action="native")]  
    return {'display':True} , children

            
            
            
application=app.server
if __name__ == '__main__':
    application.run(debug=False,port=8080)