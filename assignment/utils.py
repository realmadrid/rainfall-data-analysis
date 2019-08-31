import numpy as np
import os.path
import time
from functools import wraps


# Method B
def get_exceptionally_high_values(entries, frequency, x_set, y_set):
    """
    Find the smallest value xF in X< such that no more than n / F values in X are greater than or equal to xF. 
    In other words, xF is the (n / F):th largest value in the series.
    :param entries: the total number of years
    :param frequency: user input frequency
    :param x_set: year range
    :param y_set: rainfall amount list
    :return: threshold and a map in which key for year and value for rainfall amount
    """
    xf = entries // frequency
    y_set = np.asarray(y_set)
    threshold = sorted(y_set[~np.isnan(y_set)])[-xf]
    result = {}
    for i, val in enumerate(y_set):
        if ~np.isnan(val) and val >= threshold:
            result[x_set[i]] = val
    return threshold, result


def get_exceptionally_low_values(entries, frequency, x_set, y_set):
    xf = entries // frequency
    y_set = np.asarray(y_set)
    threshold = sorted(y_set[~np.isnan(y_set)])[xf - 1]
    result = {}
    for i, val in enumerate(y_set):
        if ~np.isnan(val) and val <= threshold:
            result[x_set[i]] = val
    return threshold, result


# Method A
def get_threshold_and_exceptional_values(x_set, y_set, frequency, condition):
    """
    Find the smallest value xF in X such that for any two values xi and xj in X, 
    if i != j, xi >= xF and xj >= xF then abs(j - i) >= F. 
    In other words, any two distinct indices where the values are greater than or equal to xF are at least F steps apart
    :param x_set: year range
    :param y_set: rainfall amount list
    :param frequency: user input frequency
    :param condition: 1 for exceptionally high and 2 for low values
    :return: threshold and a map in which key for year and value for rainfall amount
    """
    threshold = None
    result = {}
    y_set = np.asarray(y_set)
    drop_duplicate_y_set = set(y_set[~np.isnan(y_set)])
    if condition == 1:
        for x in sorted(drop_duplicate_y_set):
            if check_xf_condition(x, y_set, frequency, condition):
                threshold = x
                for i, val in enumerate(y_set):
                    if ~np.isnan(val) and val >= threshold:
                        result[x_set[i]] = val
                break
    elif condition == 2:
        for x in sorted(drop_duplicate_y_set)[::-1]:
            if check_xf_condition(x, y_set, frequency, condition):
                threshold = x
                for i, val in enumerate(y_set):
                    if ~np.isnan(val) and 0 <= val <= threshold:
                        result[x_set[i]] = val
                break
    y_set[y_set == -1] = np.nan
    if threshold is None:
        return None, None
    return threshold, result


def check_xf_condition(xf, y, f, condition):
    """
    Check whether xf is a threshold for exceptionally high or low values under frequency f.
    :param xf: the x that to be checked
    :param y: rainfall amount list
    :param f: frequency
    :param condition: 1 for exceptionally high and 2 for low values
    :return: True if xf is a valid threshold
    """
    y[np.isnan(y)] = -1
    if condition == 1:
        check_list = np.where(y >= xf)[0]
    elif condition == 2:
        check_list = np.where((y <= xf) & (y >= 0))[0]
    if len(check_list) == 1:
        return True
    else:
        for i in range(0, len(check_list) - 1):
            if abs(check_list[i] - check_list[i + 1]) < f:
                return False
        return True


def get_city_name(file_path):
    """
    Get city name from the csv file.
    :param file_path: csv file path
    :return: city name
    """
    return os.path.basename(file_path).split('_')[1]


def get_month_name(month_number):
    """
    Get the full name of a month
    :param month_number: month number
    :return: full name
    """
    if month_number == 1:
        return 'January'
    elif month_number == 2:
        return 'February'
    elif month_number == 3:
        return 'March'
    elif month_number == 4:
        return 'April'
    elif month_number == 5:
        return 'May'
    elif month_number == 6:
        return 'June'
    elif month_number == 7:
        return 'July'
    elif month_number == 8:
        return 'August'
    elif month_number == 9:
        return 'September'
    elif month_number == 10:
        return 'October'
    elif month_number == 11:
        return 'November'
    elif month_number == 12:
        return 'December'
    else:
        raise ValueError('Invalid parameter for month.')


def get_days_of_month(year, month):
    """
    Get total days of a month according to the year and month.
    :param year: Number for year
    :param month: Number for month
    :return: Total days
    """
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 29 if is_leap_year(year) else 28


def get_days_of_year(year):
    return 366 if is_leap_year(year) else 365


def is_leap_year(year):
    return True if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0) else False


def fn_timer(fun):
    """
    A decorator for printing the running time of a function.
    :param fun: Function
    :return: None
    """
    @wraps(fun)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = fun(*args, **kwargs)
        t1 = time.time()
        print("Total time running aggregation function %s: %s seconds." % (fun.__name__, str(round(t1 - t0, 2))))
        return result
    return function_timer
