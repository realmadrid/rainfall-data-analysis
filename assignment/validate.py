import numpy as np
import pandas as pd

from assignment.utils import get_days_of_month, get_days_of_year


def validate_each_month_integrity(df):
    """
    Validate the integrity of each month.
    :param df: Dataframe
    :return: A true/false list in which each element corresponds to a month,
                and a month list in which the data is incomplete.
    """
    result = []
    incomplete = []
    for index, line in df.iterrows():
        if index == 0:
            year = df.iat[0, 2]
            month = df.iat[0, 3]
            if pd.notnull(df.iat[0, 6]):
                period = df.iat[0, 6]
            elif pd.notnull(df.iat[0, 7]):
                period = 1
            else:
                period = 0
        elif index == df.index[-1]:
            if pd.notnull(df.iat[index, 6]):
                period += df.iat[index, 6]
            elif pd.notnull(df.iat[index, 7]):
                period += 1
            if period == get_days_of_month(year, month):
                result.append(True)
            else:
                result.append(False)
                incomplete.append((year, month))
            return result, incomplete
        else:
            if month != df.iat[index, 3]:
                if period == get_days_of_month(year, month):
                    result.append(True)
                else:
                    result.append(False)
                    incomplete.append((year, month))
                month = df.iat[index, 3]
                period = 0
                if year != df.iat[index, 2]:
                    year = df.iat[index, 2]
            if pd.notnull(df.iat[index, 6]):
                period += df.iat[index, 6]
            elif pd.notnull(df.iat[index, 7]):
                period += 1


def validate_specific_month_integrity(df, specific_month):
    """
    Validate the integrity of specific month.
    :param df: Dataframe
    :param specific_month: 
    :return: A true/false list in which each element corresponds to a month,
                and a month list in which the data is incomplete.
    """
    result = []
    incomplete = []
    for index, line in df.iterrows():
        if index == 0:
            year = df.iat[0, 2]
            if df.iat[0, 3] == specific_month and pd.notnull(df.iat[0, 6]):
                period = df.iat[0, 6]
            elif df.iat[0, 3] == specific_month and pd.notnull(df.iat[0, 7]):
                period = 1
            else:
                period = 0
        elif index == df.index[-1]:
            if df.iat[index, 3] == specific_month:
                if pd.notnull(df.iat[index, 6]):
                    period += df.iat[index, 6]
                elif pd.notnull(df.iat[index, 7]):
                    period += 1
            if df.iat[index, 3] >= specific_month:
                if period == get_days_of_month(year, specific_month):
                    result.append(True)
                else:
                    result.append(False)
                    incomplete.append(year)
            return result, incomplete
        else:
            if year != df.iat[index, 2]:
                if period == get_days_of_month(year, specific_month):
                    result.append(True)
                else:
                    result.append(False)
                    incomplete.append(year)
                year = df.iat[index, 2]
                period = 0
            if df.iat[index, 3] == specific_month:
                if pd.notnull(df.iat[index, 6]):
                    period += df.iat[index, 6]
                elif pd.notnull(df.iat[index, 7]):
                    period += 1


def validate_year_integrity(df):
    """
    Validate the integrity of each year.
    :param df: Dataframe
    :return: A true/false list in which each element corresponds to a year,
                and a year list in which the data is incomplete.
    """
    result = []
    incomplete = []
    for index, line in df.iterrows():
        if index == 0:
            year = df.iat[0, 2]
            if pd.notnull(df.iat[0, 6]):
                period = df.iat[0, 6]
            elif pd.notnull(df.iat[0, 7]):
                period = 1
            else:
                period = 0
        elif index == df.index[-1]:
            if pd.notnull(df.iat[index, 6]):
                period += df.iat[index, 6]
            elif pd.notnull(df.iat[index, 7]):
                period += 1
            # if period == get_days_of_year(year):  # Discard a year if the data on any day is missing
            if get_days_of_year(year) - period <= 3:  # Discard a year if more than 3 days data is missing
                result.append(True)
            else:
                result.append(False)
                incomplete.append(year)
            return result, incomplete
        else:
            if year != df.iat[index, 2]:
                # if period == get_days_of_year(year):  # Discard a year if the data on any day is missing
                if get_days_of_year(year) - period <= 3:  # Discard a year if more than 3 days data is missing
                    result.append(True)
                else:
                    result.append(False)
                    incomplete.append(year)
                year = df.iat[index, 2]
                period = 0
            if pd.notnull(df.iat[index, 6]):
                period += df.iat[index, 6]
            elif pd.notnull(df.iat[index, 7]):
                period += 1


def check_span_months_data(file_path):
    """
    Check the csv file whether a period spans more than one month.
    :param file_path: The path of csv file
    :return: None
    """
    try:
        with open(file_path, 'r', newline='') as data_file:
            df = pd.read_csv(data_file)
            df.rename(
                columns={'Product code': 'code', 'Bureau of Meteorology station number': 'station', 'Year': 'year',
                         'Month': 'month', 'Day': 'day', 'Rainfall amount (millimetres)': 'rainfall',
                         'Period over which rainfall was measured (days)': 'period', 'Quality': 'quality'},
                inplace=True)
            filter_invalid_data(df)
            filtered_data = df.loc[(df['period'] > df['day'])]
            print(filtered_data if not filtered_data.empty else 'No data spans month.')
    except IOError as err:
        print('FileNotFoundError: ' + str(err))
        exit(1)


def filter_invalid_data(df, *args):
    """
    To filter invalid data in dataframe. Set the rainfall, period, quality columns to NaN if the period column is incorrect.
    In fact, the only invalid row in three files is the period field of 2008-4-26, index 54902, in Rainfall_Sydney_066062.csv
    :param df: DataFrame, a data structure of pandas
    :return: the dataframe that has filtered invalid data
    """
    print('Checking data...')
    all_valid = True
    if args:
        for_specific_month = True
        month = args[0]
        previous = df.loc[df['month'] == month]['period'].tolist()[0]
        first_index = df.loc[df['month'] == month].index.tolist()[0]
    else:
        for_specific_month = False
    if for_specific_month:
        for index, line in df.iterrows():
            if index > first_index and df.iat[index, 3] == month:
                if previous != np.nan and line['period'] != np.nan and line['period'] > previous:
                    if all_valid:
                        all_valid = False
                    df.iat[index, 5] = np.nan  # df.columns.get_loc('rainfall') = 5
                    df.iat[index, 6] = np.nan
                    df.iat[index, 7] = np.nan
                    print('Data in %s-%s-%s is invalid, discard it.' % (df.iat[index, 4], df.iat[index, 3], df.iat[index, 2]))
            previous = line['period']
    else:
        for index, line in df.iterrows():
            if index == 0:  # Set 'previous' default value as the period value in 1st row. Alternative: index == df.index[0]
                previous = df.iat[0, 6]  # Alternative: previous = df.loc[0]['period'])
            else:
                if previous != np.nan and line['period'] != np.nan and line['period'] > previous:
                    if all_valid:
                        all_valid = False
                    df.iat[index, 5] = np.nan  # df.columns.get_loc('rainfall') = 5
                    df.iat[index, 6] = np.nan
                    df.iat[index, 7] = np.nan
                    print('Data in %s-%s-%s is invalid, discard it.' % (df.iat[index, 4], df.iat[index, 3], df.iat[index, 2]))
            previous = line['period']
        # print(df.ix[54902, :])
    if all_valid:
        print('Finished checking. All data is valid.\n')
    else:
        print('Finished checking.\n')
    return df
