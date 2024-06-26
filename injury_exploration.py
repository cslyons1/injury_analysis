#!pip install pybaseball

#interaction with os
import os

#dataframe
import pandas as pd

#data manip
import numpy as np

#various plots
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.linear_model import Ridge

#analysis
from scipy.stats import pearsonr, spearmanr, wilcoxon

#baseball data (must run pip above)
from pybaseball import statcast, playerid_lookup

#download and save csv of statcast data for each year of analysis
pitch_data_date = statcast(start_dt="date-01-01", end_dt="date-12-31")
pitch_data_date.to_csv('date_.csv')

#Create individual df's for each pitch type for each year
x_velo_2008 = velo_data_2008[(velo_data_2008['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2009 = velo_data_2009[(velo_data_2009['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2010 = velo_data_2010[(velo_data_2010['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2011 = velo_data_2011[(velo_data_2011['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2012 = velo_data_2012[(velo_data_2012['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2013 = velo_data_2013[(velo_data_2013['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2014 = velo_data_2014[(velo_data_2014['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2015 = velo_data_2015[(velo_data_2015['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2016 = velo_data_2016[(velo_data_2016['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2017 = velo_data_2017[(velo_data_2017['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2018 = velo_data_2018[(velo_data_2018['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2019 = velo_data_2019[(velo_data_2019['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2020 = velo_data_2020[(velo_data_2020['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2021 = velo_data_2021[(velo_data_2021['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2022 = velo_data_2022[(velo_data_2022['pitch_name'] == 'xx')].reset_index(drop=True)
x_velo_2023 = velo_data_2023[(velo_data_2023['pitch_name'] == 'xx')].reset_index(drop=True)

def injury_exploration(pitch_type):
  #input must be 4-Seam Fastball, Curveball, Changeup, or Slider
  pitch_type = pitch_type.title()

  #load injuries csv, skip header row to index properly
  injury_data = pd.read_csv('drive/MyDrive/Injuries Project/Tommy John Surgery List (@MLBPlayerAnalys) - TJ List.csv', skiprows=1)

  #filter data for league, add column to sum injury total by year, create df of injury data back to 2008
  position = ['P']
  level = ['MLB']
  mlb_tjs = injury_data[(injury_data['Position'].isin(position)) & (injury_data['Level'].isin(level))]

  mlb_tjs['TJ Surgery Date'] = pd.to_datetime(mlb_tjs['TJ Surgery Date'])
  mlb_tjs['Surgery Year'] = mlb_tjs['TJ Surgery Date'].dt.year

  mlb_tjs['Confirmed'] = 1
  tot_injury_yearly = mlb_tjs.loc[:,['Surgery Year', 'Confirmed']].groupby(['Surgery Year'], as_index=False).sum()

  tot_injury_yearly = tot_injury_yearly.sort_values('Surgery Year')

  cutoff = 2008
  limit = 2024
  chart_data = tot_injury_yearly[(tot_injury_yearly['Surgery Year'] >= cutoff) & (tot_injury_yearly['Surgery Year'] < limit)]

  chart_data['Surgery Year'] = chart_data['Surgery Year'].astype(str)

  years = np.array([2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
  cd_for_df = np.array(chart_data['Confirmed'])

  #creating df and ploting based on 4-seam pitch type input
  if pitch_type == '4-Seam Fastball':

    fs_velos = pd.read_csv('/content/drive/MyDrive/Injuries Project/fs_velos.csv')

    fs_v_totals = fs_velos.loc[:,['2008_velo','2009_velo','2010_velo','2011_velo','2012_velo','2013_velo','2014_velo','2015_velo','2016_velo','2017_velo','2018_velo','2019_velo','2020_velo','2021_velo','2022_velo','2023_velo']].median()
    nump_fs_v_totals = np.array(fs_v_totals)

    fs_velos['Velocities'] = pd.concat([fs_velos['2008_velo'],fs_velos['2009_velo'],fs_velos['2010_velo'],
                                        fs_velos['2011_velo'],fs_velos['2012_velo'],fs_velos['2013_velo'],
                                        fs_velos['2014_velo'],fs_velos['2015_velo'],fs_velos['2016_velo'],
                                        fs_velos['2017_velo'],fs_velos['2018_velo'],fs_velos['2019_velo'],
                                        fs_velos['2020_velo'],fs_velos['2021_velo'],fs_velos['2022_velo'],
                                        fs_velos['2023_velo']], ignore_index=True)

    df_ = pd.DataFrame({'Year':years, 'Median Velocity':fs_v_totals, 'Confirmed Surgeries':cd_for_df}).reset_index(drop=True)

    sr = spearmanr(df_['Confirmed Surgeries'], df_['Median Velocity'])
    sr2 = sr[0]**2

    sns.set_theme(style='whitegrid', font_scale=.75, rc={'figure.figsize':(15,10)})
    fig, ax = plt.subplots()
    lr = Ridge()

    vel_ = mpatches.Patch(color='red', label='Velocities')
    surg_ = mpatches.Patch(color='blue', label='Surgeries')

    plt.bar(df_['Year'], df_['Median Velocity'], width=.45, color='coral', align='center')
    plt.ylim(90,95)
    lr.fit(df_[['Year']], df_['Median Velocity'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='red')
    ax.set_ylabel('Median Velocity (MPH)')
    ax.set_xlabel('Year')

    ax2 = ax.twinx()
    plt.bar(df_['Year'], df_['Confirmed Surgeries'], width=.45, color='steelblue', align='edge')
    plt.ylim(8,60)
    ax2.grid(False)
    lr.fit(df_[['Year']], df_['Confirmed Surgeries'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='blue')
    ax2.set_ylabel('Confirmed Surgeries')

    plt.legend(handles=[vel_,surg_], loc='upper left')
    title_str = f"""
                'Relationship Between Increasing {pitch_type} Velocities & Tommy John Surgeries from 2008 to 2023'
                Spearman: {round(sr[0], 3)} (SR2: {round(sr2, 3)}, p= {round(sr[-1], 3)})
                """
    ax.set_title(title_str)

    return plt.show()

  #creating df and plotting based on Curveball pitch type input
  elif pitch_type == 'Curveball':

    curve_velos = pd.read_csv('/content/drive/MyDrive/Injuries Project/curve_velos.csv')

    curve_v_totals = curve_velos.loc[:,['2008_velo','2009_velo','2010_velo','2011_velo','2012_velo','2013_velo','2014_velo','2015_velo','2016_velo','2017_velo','2018_velo','2019_velo','2020_velo','2021_velo','2022_velo','2023_velo']].median()
    nump_curve_v_totals = np.array(curve_v_totals)

    curve_velos['Velocities'] = pd.concat([curve_velos['2008_velo'],curve_velos['2009_velo'],curve_velos['2010_velo'],
                                        curve_velos['2011_velo'],curve_velos['2012_velo'],curve_velos['2013_velo'],
                                        curve_velos['2014_velo'],curve_velos['2015_velo'],curve_velos['2016_velo'],
                                        curve_velos['2017_velo'],curve_velos['2018_velo'],curve_velos['2019_velo'],
                                        curve_velos['2020_velo'],curve_velos['2021_velo'],curve_velos['2022_velo'],
                                        curve_velos['2023_velo']], ignore_index=True)

    df_ = pd.DataFrame({'Year':years, 'Median Velocity':curve_v_totals, 'Confirmed Surgeries':cd_for_df}).reset_index(drop=True)

    sr = spearmanr(df_['Confirmed Surgeries'], df_['Median Velocity'])
    sr2 = sr[0]**2

    sns.set_theme(style='whitegrid', font_scale=.75, rc={'figure.figsize':(15,10)})
    fig, ax = plt.subplots()
    lr = Ridge()

    vel_ = mpatches.Patch(color='red', label='Velocities')
    surg_ = mpatches.Patch(color='blue', label='Surgeries')

    plt.bar(df_['Year'], df_['Median Velocity'], width=.45, color='coral', align='center')
    plt.ylim(74,80)
    lr.fit(df_[['Year']], df_['Median Velocity'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='red')
    ax.set_ylabel('Median Velocity (MPH)')
    ax.set_xlabel('Year')

    ax2 = ax.twinx()
    plt.bar(df_['Year'], df_['Confirmed Surgeries'], width=.45, color='steelblue', align='edge')
    plt.ylim(8,60)
    ax2.grid(False)
    lr.fit(df_[['Year']], df_['Confirmed Surgeries'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='blue')
    ax2.set_ylabel('Confirmed Surgeries')

    plt.legend(handles=[vel_,surg_], loc='upper left')
    title_str = f"""
                'Relationship Between Increasing {pitch_type} Velocities & Tommy John Surgeries from 2008 to 2023'
                Spearman: {round(sr[0], 3)} (SR2: {round(sr2, 3)}, p= {round(sr[-1], 3)})
                """
    ax.set_title(title_str)

    return plt.show()

  #creating df and plotting based on Changeup pitch type input
  elif pitch_type == 'Changeup':

    change_velos = pd.read_csv('/content/drive/MyDrive/Injuries Project/change_velos.csv')

    change_v_totals = change_velos.loc[:,['2008_velo','2009_velo','2010_velo','2011_velo','2012_velo','2013_velo','2014_velo','2015_velo','2016_velo','2017_velo','2018_velo','2019_velo','2020_velo','2021_velo','2022_velo','2023_velo']].median()
    nump_change_v_totals = np.array(change_v_totals)

    change_velos['Velocities'] = pd.concat([change_velos['2008_velo'],change_velos['2009_velo'],change_velos['2010_velo'],
                                        change_velos['2011_velo'],change_velos['2012_velo'],change_velos['2013_velo'],
                                        change_velos['2014_velo'],change_velos['2015_velo'],change_velos['2016_velo'],
                                        change_velos['2017_velo'],change_velos['2018_velo'],change_velos['2019_velo'],
                                        change_velos['2020_velo'],change_velos['2021_velo'],change_velos['2022_velo'],
                                        change_velos['2023_velo']], ignore_index=True)

    df_ = pd.DataFrame({'Year':years, 'Median Velocity':change_v_totals, 'Confirmed Surgeries':cd_for_df}).reset_index(drop=True)

    sr = spearmanr(df_['Confirmed Surgeries'], df_['Median Velocity'])
    sr2 = sr[0]**2

    sns.set_theme(style='whitegrid', font_scale=.75, rc={'figure.figsize':(15,10)})
    fig, ax = plt.subplots()
    lr = Ridge()

    vel_ = mpatches.Patch(color='red', label='Velocities')
    surg_ = mpatches.Patch(color='blue', label='Surgeries')

    plt.bar(df_['Year'], df_['Median Velocity'], width=.45, color='coral', align='center')
    plt.ylim(80,86)
    lr.fit(df_[['Year']], df_['Median Velocity'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='red')
    ax.set_ylabel('Median Velocity (MPH)')
    ax.set_xlabel('Year')

    ax2 = ax.twinx()
    plt.bar(df_['Year'], df_['Confirmed Surgeries'], width=.45, color='steelblue', align='edge')
    plt.ylim(8,60)
    ax2.grid(False)
    lr.fit(df_[['Year']], df_['Confirmed Surgeries'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='blue')
    ax2.set_ylabel('Confirmed Surgeries')

    plt.legend(handles=[vel_,surg_], loc='upper left')
    title_str = f"""
                'Relationship Between Increasing {pitch_type} Velocities & Tommy John Surgeries from 2008 to 2023'
                Spearman: {round(sr[0], 3)} (SR2: {round(sr2, 3)}, p= {round(sr[-1], 3)})
                """
    ax.set_title(title_str)

    return plt.show()

  #plotting based on Slider pitch type input
  elif pitch_type == 'Slider':

    slider_velos = pd.read_csv('/content/drive/MyDrive/Injuries Project/slider_velos.csv')

    slider_v_totals = slider_velos.loc[:,['2008_velo','2009_velo','2010_velo','2011_velo','2012_velo','2013_velo','2014_velo','2015_velo','2016_velo','2017_velo','2018_velo','2019_velo','2020_velo','2021_velo','2022_velo','2023_velo']].median()
    nump_slider_v_totals = np.array(slider_v_totals)

    slider_velos['Velocities'] = pd.concat([slider_velos['2008_velo'],slider_velos['2009_velo'],slider_velos['2010_velo'],
                                        slider_velos['2011_velo'],slider_velos['2012_velo'],slider_velos['2013_velo'],
                                        slider_velos['2014_velo'],slider_velos['2015_velo'],slider_velos['2016_velo'],
                                        slider_velos['2017_velo'],slider_velos['2018_velo'],slider_velos['2019_velo'],
                                        slider_velos['2020_velo'],slider_velos['2021_velo'],slider_velos['2022_velo'],
                                        slider_velos['2023_velo']], ignore_index=True)

    df_ = pd.DataFrame({'Year':years, 'Median Velocity':slider_v_totals, 'Confirmed Surgeries':cd_for_df}).reset_index(drop=True)

    sr = spearmanr(df_['Confirmed Surgeries'], df_['Median Velocity'])
    sr2 = sr[0]**2

    sns.set_theme(style='whitegrid', font_scale=.75, rc={'figure.figsize':(15,10)})
    fig, ax = plt.subplots()
    lr = Ridge()

    vel_ = mpatches.Patch(color='red', label='Velocities')
    surg_ = mpatches.Patch(color='blue', label='Surgeries')

    plt.bar(df_['Year'], df_['Median Velocity'], width=.45, color='coral', align='center')
    plt.ylim(82,86)
    lr.fit(df_[['Year']], df_['Median Velocity'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='red')
    ax.set_ylabel('Median Velocity (MPH)')
    ax.set_xlabel('Year')

    ax2 = ax.twinx()
    plt.bar(df_['Year'], df_['Confirmed Surgeries'], width=.45, color='steelblue', align='edge')
    plt.ylim(8,60)
    ax2.grid(False)
    lr.fit(df_[['Year']], df_['Confirmed Surgeries'])
    plt.plot(df_['Year'], lr.coef_*df_['Year']+lr.intercept_, color='blue')
    ax2.set_ylabel('Confirmed Surgeries')

    plt.legend(handles=[vel_,surg_], loc='upper left')
    title_str = f"""
                'Relationship Between Increasing {pitch_type} Velocities & Tommy John Surgeries from 2008 to 2023'
                Spearman: {round(sr[0], 3)} (SR2: {round(sr2, 3)}, p= {round(sr[-1], 3)})
                """
    ax.set_title(title_str)

    return plt.show()

  else:
    return print("Please retry using one of the following pitch types: '4-Seam Fastball', 'Curveball', 'Changeup', or 'Slider'")