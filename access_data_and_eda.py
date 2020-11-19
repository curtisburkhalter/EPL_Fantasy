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
import seaborn as sns
from matplotlib import rcParams
import matplotlib.pyplot as plt

# set figure size in inches
rcParams['figure.figsize'] = 11.7,8.27

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

#create dataframes by position and sort by highest roi
gk_df = elements_active[elements_active['position'] == 'Goalkeeper'].copy().sort_values(by = 'roi', ascending = False)
gk_sub = gk_df[['minutes','goals_conceded','clean_sheets','chance_of_playing_next_round','chance_of_playing_this_round', 'penalties_saved','saves', 'first_name','second_name','points_per_game','value_form', 'total_points','value_season','roi','now_cost']].copy()
gk_sub['player'] = gk_sub['first_name'] + " " +  gk_sub['second_name']

mf_df = elements_active[elements_active['position'] == 'Midfielder'].copy().sort_values(by = 'roi', ascending = False)
mf_sub = mf_df[['assists','creativity_rank','chance_of_playing_next_round','chance_of_playing_this_round', 'minutes','penalties_missed', 'threat_rank', 'first_name','second_name','points_per_game','value_form', 'total_points','value_season','roi','now_cost']].copy()
mf_sub['player'] = mf_sub['first_name'] + " " + mf_sub['second_name']

fwd_df = elements_active[elements_active['position'] == 'Forward'].copy().sort_values(by = 'roi', ascending = False)
fwd_sub = fwd_df[['assists','creativity_rank','chance_of_playing_next_round','chance_of_playing_this_round', 'minutes','penalties_missed', 'threat_rank', 'first_name','second_name','points_per_game','value_form', 'total_points','value_season','roi','now_cost']].copy()
fwd_sub['player'] = fwd_sub['first_name'] + " " + fwd_sub['second_name']

def_df = elements_active[elements_active['position'] == 'Defender'].copy().sort_values(by = 'roi', ascending = False)
def_sub = def_df[['assists','creativity_rank','chance_of_playing_next_round','chance_of_playing_this_round', 'minutes','yellow_cards','red_cards', 'threat_rank', 'first_name','second_name','points_per_game','value_form', 'total_points','value_season','roi','now_cost']].copy()
def_sub['player'] = def_sub['first_name'] + " " + def_sub['second_name']


#create barplots to look at graphical representation of position dataframes by roi
plt.figure()
sns.barplot(x="roi", y="player", data=gk_sub)

plt.figure()
sns.barplot(x="roi", y="player", data=mf_sub.iloc[0:20,:])

plt.figure()
sns.barplot(x="roi", y="player", data=fwd_sub.iloc[0:20,:])

plt.figure()
sns.barplot(x="roi", y="player", data=def_sub.iloc[0:20,:])

#correlation function
def corr_hp(df):
    
#look at correlations between variables
# Compute the correlation matrix
    df_corr = df.corr()

# Generate a mask for the upper triangle
    df_mask = np.triu(np.ones_like(df_corr, dtype=bool))

# Draw the heatmap with the mask and correct aspect ratio
    return sns.heatmap(df_corr, mask=df_mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.figure()
corr_hp(gk_sub)
plt.figure()
corr_hp(mf_sub)
plt.figure()
corr_hp(fwd_sub)
plt.figure()
corr_hp(def_sub)
