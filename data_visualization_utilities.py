"""
This file contains all utility functions used in the "Data Analysis & Visualization" Notebook
Stephen Kaplan, 2020-07-05
"""
import matplotlib.pyplot as plt
import seaborn as sns


def get_top_stations_by_total_traffic(df, num_stations=10):
    """
    Returns a DataFrame containing the busiest stations by total traffic.

    :param pandas.DataFrame df: MTA turnstile data. Must contain columns STATION and TOTAL_TRAFFIC.
    :param int num_stations: Number of busiest stations to return. Defaults to 10.
    :return: DataFrame containing the top n busiest stations.
    :rtype: pandas.DataFrame
    """
    # aggregate total traffic for each station and sort in descending order
    df_grouped_by_stations = df.groupby('STATION', as_index=False).sum()
    df_stations_ranked = df_grouped_by_stations.sort_values('TOTAL_TRAFFIC', ascending=False)

    return df_stations_ranked[0:num_stations]


def prepare_mta_data_for_heatmap(df):
    """
    Prepares MTA turnstile data to plot a heatmap of traffic at different stations during different times of day.

    :param pandas.DataFrame df: Contains columns STATION, DATE, TIME_BIN, TOTAL_TRAFFIC, TIME
    :return: DataFrame with average traffic by 3-hour time increments.
    :rtype: pandas.DataFrame
    """
    # total entries at each station on each date for each 3-hr timespan
    hour_bin_sum = df.groupby(['STATION', 'DATE', 'TIME_BIN']).agg({'TOTAL_TRAFFIC': 'sum'})
    hour_bin_sum.reset_index(inplace=True)

    # Use amounts above to calculate the average entries in each 3-hr timespan at each station
    hourly_avg_df = hour_bin_sum.groupby(['TIME_BIN', 'STATION']).agg({'TOTAL_TRAFFIC': 'mean'})
    hourly_avg_df.reset_index(inplace=True)

    # Put data in hourly_avg_df in format conducive for line plots
    df_heatmap = hourly_avg_df.pivot_table(index='STATION', columns='TIME_BIN', values='TOTAL_TRAFFIC')

    return df_heatmap


def plot_busy_times_heatmap(df, title):
    """
    Plots a heatmap of the average busiest time spans at a given set of stations.

    :param df: DataFrame that has been prepared by the function prepare_mta_data_for_heatmap
    :param str title: Plot title.
    """
    plt.figure(figsize=(16, 12))
    sns.heatmap(df, vmin=2500, vmax=40000, cbar_kws={'label': 'Avg Total Traffic'})
    plt.xlabel('3-Hour Windows', fontsize=14)
    plt.ylabel('Stations', fontsize=14)
    plt.title(title, fontsize=20)
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8],
               ['12:00am - 3:00am', '3:00am - 6:00am', '6:00am - 9:00am', '9:00am - 12:00pm',
                '12:00pm - 3:00pm', '3:00pm - 6:00pm', '6:00pm - 9:00pm', '9:00pm - 12:00am'],
               rotation=45)
