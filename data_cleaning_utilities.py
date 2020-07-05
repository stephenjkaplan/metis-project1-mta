"""
This file contains all utility functions used in the "Data Acquisition & Cleaning" Notebook
Stephen Kaplan, 2020-07-05
"""
import numpy as np
import pandas as pd


def convert_timestamp_to_mta_format(timestamp):
    """
    Converts pandas timestamp to expected string format of date in MTA Turnstile data URLs: "YYMMDD".

    :param pandas.Timestamp timestamp: Full date as a pandas Timestamp object.
    :return: Date in format YYMMDD
    :rtype: str
    """
    # convert year to last 2 digits
    year = str(timestamp.year)[2:4]

    # zero-pad the month and day if only one digit
    month = str(timestamp.month).zfill(2)
    day = str(timestamp.day).zfill(2)

    date_mta_format = year + month + day

    return date_mta_format


def get_mta_turnstile_data(start, end, months_of_interest):
    """
    Gets MTA turnstile data (http://web.mta.info/developers/turnstile.html) for a specified start/end date, within
    a range of months. Combines data into a single dataframe as output.

    :param str start: First date to pull data for in format 'YYYY-MM-DD'.
                      Must match the date of a data file at the above URL.
    :param str end: Last date to pull data for in format 'YYYY-MM-DD'
                    Must match the date of a data file at the above URL.
    :param list months_of_interest: Contains integer values corresponding to the months out of every year that data
                                     should be pulled for (January = 1, ... , December=12).
    :return: All requested MTA turnstile data concatenated into a single data frame.
    :rtype: pandas.DataFrame
    """
    # create range of dates to pull data for and initialize data frame to store all combined data. data is stored weekly
    date_range = pd.date_range(start, end, freq='7D')
    df_turnstile_data = pd.DataFrame()

    # iterate through range of dates, ignoring dates if they do not fall in the months of interest
    for date in date_range:
        if date.month in months_of_interest:
            print(f'Downloading data for {date}...')
            date_formatted = convert_timestamp_to_mta_format(date)

            # load data and concatenate to combined dataframe
            url = f'http://web.mta.info/developers/data/nyct/turnstile/turnstile_{date_formatted}.txt'
            df_turnstile_data_week = pd.read_csv(url)
            df_turnstile_data = pd.concat([df_turnstile_data, df_turnstile_data_week])

    return df_turnstile_data


def clean_hourly_turnstile_traffic(turnstile_data_row, reset_limit, entries=True):
    """
    Calculates hourly turnstile traffic (entries or exits) using current day and previous day readings.
    Adjusts for erroneous reverse counting and turnstile count resets.

    :param pandas.Series turnstile_data_row: Row of data corresponding to a single 4-hour span of
                                             data for a single turnstile.
    :param int reset_limit: Used as an upper limit to determine if turnstile reset.
    :param bool entries: If True, uses turnstile entries in calculation. If False, uses turnstile exits.
    :return: Total hourly traffic (entries or exits) for a single turnstile.
    :rtype: int
    """
    traffic_type = 'ENTRIES' if entries else 'EXITS'

    hourly_traffic = turnstile_data_row["HOURLY_" + traffic_type]

    # reverse sign again if median is negative
    hourly_traffic = -hourly_traffic if hourly_traffic < 0 else hourly_traffic

    # if counter was possibly reset to 0, set to median value for that turnstile/day of week/time
    if hourly_traffic > reset_limit:
        hourly_traffic = abs(turnstile_data_row[traffic_type + "_MEDIAN"])

    # if the reset limit is still reached with median, set to NaN
    if hourly_traffic > reset_limit:
        hourly_traffic = np.nan

    return hourly_traffic
