from assignment.validate import *
from assignment.utils import fn_timer

# Rename the columns
columns = {'Product code': 'code', 'Bureau of Meteorology station number': 'station', 'Year': 'year',
           'Month': 'month', 'Day': 'day', 'Rainfall amount (millimetres)': 'rainfall',
           'Period over which rainfall was measured (days)': 'period', 'Quality': 'quality'}


@fn_timer
def total_for_each_month(file_path):
    """
    Calculate the total rainfall amount for each month.
    :param file_path: The path of csv file
    :return: Month range list, the aggregate rainfall amount list, incomplete year&month list
    """
    try:
        with open(file_path, 'r') as data_file:
            df = pd.read_csv(data_file)
            df.rename(columns=columns, inplace=True)
            df = filter_invalid_data(df)
            validate, incomplete = validate_each_month_integrity(df)  # Validate data integrity
            filtered_data = df.loc[:, ['year', 'month', 'rainfall']]  # Select target columns
            grouped = filtered_data['rainfall'].groupby([filtered_data['year'], filtered_data['month']]).sum()
            month_set = [tuple(x) for x in filtered_data[['year', 'month']].drop_duplicates().values.tolist()]
            for i in range(len(validate)):
                if not validate[i]:
                    grouped.iat[i] = np.nan
            return month_set, grouped.tolist(), incomplete
    except IOError as err:
        print('FileNotFoundError: ' + str(err))
        exit(1)


@fn_timer
def total_for_specific_month(file_path, specific_month):
    """
    Calculate the total rainfall amount for specific month.
    :param file_path: The path of csv file
    :param specific_month: The month user input
    :return: Year range list, the aggregate rainfall amount list, incomplete year list
    """
    try:
        with open(file_path, 'r') as data_file:
            df = pd.read_csv(data_file)
            df.rename(columns=columns, inplace=True)
            df = filter_invalid_data(df, specific_month)  # Validate data integrity
            validate, incomplete = validate_specific_month_integrity(df, specific_month)
            filtered_data = df.loc[(df['month'] == specific_month), ['year', 'rainfall']]
            grouped = filtered_data['rainfall'].groupby(filtered_data['year']).sum()
            for i in range(len(validate)):
                if not validate[i]:
                    grouped.iat[i] = np.nan
            return np.arange(filtered_data['year'].min(), filtered_data['year'].max() + 1), grouped.tolist(), incomplete
            # Alternative ways to get year list: 1. filtered_data['year'].drop_duplicates().values.tolist()
            #                                    2. list(set(filtered_data['year']))
    except IOError as err:
        print('FileNotFoundError: ' + str(err))
        exit(1)


@fn_timer
def total_for_each_year(file_path):
    """
    Calculate the total rainfall amount for each year.
    :param file_path: The path of csv file
    :return: Year range list, the aggregate rainfall amount list, incomplete year list
    """
    try:
        with open(file_path, 'r') as data_file:
            df = pd.read_csv(data_file)
            df.rename(columns=columns, inplace=True)
            df = filter_invalid_data(df)
            validate, incomplete = validate_year_integrity(df)  # Validate data integrity
            filtered_data = df.loc[:, ['year', 'rainfall']]
            grouped = filtered_data['rainfall'].groupby(filtered_data['year']).sum()
            for i in range(len(validate)):
                if not validate[i]:
                    grouped.iat[i] = np.nan
            return np.arange(filtered_data['year'].min(), filtered_data['year'].max() + 1), grouped.tolist(), incomplete
    except IOError as err:
        print('FileNotFoundError: ' + str(err))
        exit(1)


def each_single_day(file_path):
    """
    Obtain a dataframe which contains only daily observation.
    :param file_path: The path of csv file
    :return: Filtered dataframe
    """
    try:
        with open(file_path, 'r') as data_file:
            df = pd.read_csv(data_file)
            df.rename(columns=columns, inplace=True)
            df.loc[df['period'] > 1, ['rainfall']] = np.nan
            return df[['year', 'month', 'day', 'rainfall']]
    except IOError as err:
        print('FileNotFoundError: ' + str(err))
        exit(1)
