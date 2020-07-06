# To show what libraries I used
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


''' 
1) create df for 10 busiest stations
2) Filter out 2015 data due to station name inconsistencies 
3) Extract components of timestamps
'''
df_for_viz = mta_raw_data[(mta_raw_data['YEAR'] > 2015) &
                          mta_raw_data['STATION'].isin(station_selection)].copy()
df_for_viz["Week"] = df_for_viz.DATETIME.dt.week
df_for_viz["dayofweek"] = df_for_viz.DATETIME.dt.dayofweek
df_for_viz['Hour'] = df_for_viz['DATETIME'].dt.hour
# Separate reporting times into 3-hr bins
df_for_viz['Time_bin'] = pd.cut(df_for_viz['Hour'], 8, precision=0)

# Calculate average entries by day of week and structure data for graphing
agg_dayofweek_df = df_for_viz.groupby(['STATION', 'YEAR', 'DATE'], as_index=False).agg({'ENTRIES_DELTA':'sum'})
agg_dayofweek_df['DAY_OF_WEEK'] = agg_dayofweek_df['DATE'].dt.dayofweek
day_of_week_avg = agg_dayofweek_df.groupby(['STATION', 'DAY_OF_WEEK'], as_index=False).agg({'ENTRIES_DELTA':'mean'})
dow_avg_graph = day_of_week_avg.pivot_table(index='DAY_OF_WEEK', columns='STATION', values='ENTRIES_DELTA')

# Plot average entries by day of week
dow_avg_graph.plot(figsize=(16,10))
plt.xlabel('Day of Week', fontsize=14)
plt.ylabel('Average Entries', fontsize=14)
plt.title('For Top 10 Stations (May-Jun for 2015-2020)', fontsize=20)
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])

# Two DFs: 1) data for weekdays; 2) data for weekend
hours_weekday_df = df_for_viz[df_for_viz['dayofweek'].isin(range(6))]
hours_weekend_df = df_for_viz[df_for_viz['dayofweek'].isin(range(5,7))]

def hourly_avg_graph_data(df):
    ''' Returns df with average entries by 3-hour time increments
    arg: 
        dataframe in df_for_viz format. Column names must match
    return:
        dataframe used for heatmap
    '''
    # total entries at each station on each date for each 3-hr timespan
    hour_bin_sum = df.groupby(['STATION', 'DATE', 'Time_bin']).agg({'ENTRIES_DELTA': 'sum'})
    hour_bin_sum.reset_index(inplace=True)

    # Use amounts above to calculate the average entries in each 3-hr timespan at each station
    hourly_avg_df = hour_bin_sum.groupby(['Time_bin', 'STATION']).agg({'ENTRIES_DELTA': 'mean'})
    hourly_avg_df.reset_index(inplace=True)

    # Put data in hourly_avg_df in format conducive for line plots
    hourly_avg_graph = hourly_avg_df.pivot_table(index='STATION', columns='Time_bin', values='ENTRIES_DELTA')
    
    return hourly_avg_graph
weekday_graph = hourly_avg_graph_data(hours_weekday_df)
weekend_graph = hourly_avg_graph_data(hours_weekend_df)

# Weekday 3-hr span heatmap - Include this graph in deck only
plt.suptitle('Weekday for Top 10 Stations (May-Jun for 2016-2020)', fontsize=30)
plt.figure(figsize=(16, 12))
sns.heatmap(weekday_graph, vmin=2500, vmax=40000, cbar_kws={'label': 'Avg Entries'})
plt.xlabel('3-Hour Windows', fontsize=14)
plt.ylabel('Average Entries', fontsize=14)
plt.title('Weekday', fontsize=20)
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], ['12:00am - 3:00am', '3:00am - 6:00am',
                                '6:00am - 9:00am', '9:00am - 12:00pm',
                                '12:00pm - 3:00pm', '3:00pm - 6:00pm',
                                '6:00pm - 9:00pm', '9:00pm - 12:00am'], rotation=45)

# Weekend 3-hr span heatmap - Do not include in deck
plt.figure(figsize=(16,12))
sns.heatmap(weekend_graph, vmin=2500, vmax=40000)
plt.xlabel('3-Hour Windows', fontsize=14)
plt.ylabel('Stations', fontsize=14)
plt.title('Weekend', fontsize=20)
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], ['12:00am - 3:00am', '3:00am - 6:00am',
                                '6:00am - 9:00am', '9:00am - 12:00pm',
                                '12:00pm - 3:00pm', '3:00pm - 6:00pm',
                                '6:00pm - 9:00pm', '9:00pm - 12:00am'], rotation=45)
