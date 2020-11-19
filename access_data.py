# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 14:43:20 2020

@author: curtis burkhalter

"""

#access data from the EPL fantasy API

#import necessary packages
import requests
import pandas as pd
import numpy as np

#specify api url
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

#make a GET request from api

r = requests.get(url)

#transform request into a json
json = r.json()

#look at json keys
json.keys()

#build dataframes from keys
elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])
stats_df = pd.DataFrame(json['element_stats'])

#map the player position from 'elements_types_df' to 'elements_df'
elements_df['position'] = elements_df.element_type.map(elements_types_df.set_index('id').singular_name)

#map the player team from 'teams_df' to elements_df
elements_df['team'] = elements_df.team.map(teams_df.set_index('id').name)

#convert value_season to a float. 
#'value_season' is the value assigned to a player by the EPL Fantasy program
elements_df['value_season'] = elements_df['value_season'].astype(float)

#create a ROI column by dividing a player's total points by their 'now_cost'
elements_df['roi']  = elements_df['total_points']/elements_df['now_cost']

#remove players that have played zero minutes this season
elements_active = elements_df[elements_df['minutes'] > 0]

#look at value by position
pos_values = elements_active.groupby('position')['value_season'].mean()

#look at value by team
team_values = elements_active.groupby('team')['value_season'].mean()
