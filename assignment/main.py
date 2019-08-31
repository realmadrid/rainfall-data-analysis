import matplotlib.pyplot as mpl

from assignment.aggregate import *
from assignment.utils import *


input_str1 = input('Please enter the path to the data file:\n')
input_path = str(input_str1)
city = get_city_name(input_path)
input_str2 = input('Select the type of time series aggregation:\n1 - The total for each month.\n'
                   '2 - The total for a specific month of the year.\n3 - The total for each year.\n4 - Single day.\n')
input_type = int(input_str2)
if input_type == 2:
    input_str3 = input('Enter a specific month(1 ~ 12):\n')
    input_month = int(input_str3)

input_str4 = input('Select whether to compute a threshold for exceptionally high or low values:\n'
                   '1 - Compute a threshold for exceptionally high values.\n'
                   '2 - Compute a threshold for exceptionally low values.\n')
select_frequency = int(input_str4)

input_str5 = input('Please enter the frequency F:\n')
input_frequency = int(input_str5)

print('Running... Please wait a few seconds...')

if input_type == 1:
    month_set, y, incomplete_months = total_for_each_month(input_path)
    if incomplete_months:
        print('\nNotice: \nThe data of months', ', '.join(str(x) for x in incomplete_months), 'is incomplete so the total amount for these months cannot be computed.\n')

    if select_frequency == 1:
        t1, result1 = get_threshold_and_exceptional_values(month_set, y, input_frequency, 1)  # Method A
        if t1 is None:
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in %s months maximum rainfall of %s:' % (input_frequency, city))
            for (k, v) in result1.items():
                print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_high_values(len(month_set), input_frequency, month_set, y)  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in %s months maximum rainfall of %s:' % (input_frequency, city))
        for (k, v) in result2.items():
            print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')
    elif select_frequency == 2:
        t1, result1 = get_threshold_and_exceptional_values(month_set, y, input_frequency, 2)  # Method A
        if t1 is None:
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in %s months driest month of %s:' % (input_frequency, city))
            for (k, v) in result1.items():
                print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_low_values(len(month_set), input_frequency, month_set, y)  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in %s months driest month of %s:' % (input_frequency, city))
        for (k, v) in result2.items():
            print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')

if input_type == 2:
    years, y, incomplete_years = total_for_specific_month(input_path, input_month)
    if incomplete_years:
        print('\nNotice: \nThe data of years', ', '.join(str(x) for x in incomplete_years), 'is incomplete so the total amount for these years cannot be computed.\n')
    a_fail = False
    if select_frequency == 1:
        t1, result1 = get_threshold_and_exceptional_values(years, y, input_frequency, 1)  # Method A
        if t1 is None:
            a_fail = True
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in', input_frequency, 'years maximum rainfall for the month of', get_month_name(input_month), ':')
            for (k, v) in result1.items():
                print(k, 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_high_values(years.size, input_frequency, years, y)  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in', input_frequency, 'years maximum rainfall for the month of', get_month_name(input_month), ':')
        for (k, v) in result2.items():
            print(k, 'rainfall:', round(v, 1), 'mm')
    elif select_frequency == 2:
        t1, result1 = get_threshold_and_exceptional_values(years, y, input_frequency, 2)  # Method A
        if t1 is None:
            a_fail = True
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in', input_frequency, 'years driest year for the month of', get_month_name(input_month), ':')
            for (k, v) in result1.items():
                print(k, 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_low_values(years.size, input_frequency, years, y)  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in', input_frequency, 'years driest year for the month of', get_month_name(input_month), ':')
        for (k, v) in result2.items():
            print(k, 'rainfall:', round(v, 1), 'mm')
    x = np.arange(0, len(y))
    mpl.figure(figsize=(20, 6))
    # mng = mpl.get_current_fig_manager()
    # mng.window.showMaximized()  # To maximize the window
    mpl.bar(x + 0.25, y, 0.5, color='blue')
    if not a_fail:
        mpl.plot([0, len(y)], [t1, t1], color="black", linewidth=1.0, linestyle="-.", label="Method A")
    mpl.plot([0, len(y)], [t2, t2], color="red", linewidth=1.0, linestyle="--", label="Method B")
    mpl.legend(loc='best')
    mpl.xticks(x + 0.25, years, rotation=90)
    mpl.show()

if input_type == 3:
    years, y, incomplete_years = total_for_each_year(input_path)
    if incomplete_years:
        print('\nNotice: \nThe data of years', ', '.join(str(x) for x in incomplete_years), 'is incomplete so the total amount for these years cannot be computed.\n')
    a_fail = False
    if select_frequency == 1:
        t1, result1 = get_threshold_and_exceptional_values(years, y, input_frequency, 1)  # Method A
        if t1 is None:
            a_fail = True
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in %s years maximum rainfall of %s:' % (input_frequency, city))
            for (k, v) in result1.items():
                print(k, 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_high_values(years.size, input_frequency, years, y)  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in %s years maximum rainfall of %s:' % (input_frequency, city))
        for (k, v) in result2.items():
            print(k, 'rainfall:', round(v, 1), 'mm')
    elif select_frequency == 2:
        t1, result1 = get_threshold_and_exceptional_values(years, y, input_frequency, 2)  # Method A
        if t1 is None:
            a_fail = True
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in %s years driest year of %s:' % (input_frequency, city))
            for (k, v) in result1.items():
                print(k, 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_low_values(years.size, input_frequency, years, y)  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in %s years driest year of %s:' % (input_frequency, city))
        for (k, v) in result2.items():
            print(k, 'rainfall:', round(v, 1), 'mm')
    x = np.arange(0, len(y))
    mpl.figure(figsize=(20, 6))
    mpl.bar(x + 0.25, y, 0.5, color='blue')
    if not a_fail:
        mpl.plot([0, len(y)], [t1, t1], color="black", linewidth=1.0, linestyle="-.", label="Method A")
    mpl.plot([0, len(y)], [t2, t2], color="red", linewidth=1.0, linestyle="--", label="Method B")
    mpl.legend(loc='best')
    mpl.xticks(x + 0.25, years, rotation=90)
    mpl.show()

if input_type == 4:
    df = each_single_day(input_path)
    date_set = [tuple(x) for x in df[['year', 'month', 'day']].values.tolist()]
    if select_frequency == 1:
        t1, result1 = get_threshold_and_exceptional_values(date_set, df['rainfall'], input_frequency, 1)  # Method A
        if t1 is None:
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in %s days maximum rainfall of %s:' % (input_frequency, city))
            for (k, v) in result1.items():
                print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_high_values(len(df.index), input_frequency, date_set, df['rainfall'])  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in %s days maximum rainfall of %s:' % (input_frequency, city))
        for (k, v) in result2.items():
            print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')
    elif select_frequency == 2:
        t1, result1 = get_threshold_and_exceptional_values(date_set, df['rainfall'], input_frequency, 2)  # Method A
        if t1 is None:
            print('Method A failed under current frequency.\n')
        else:
            print('Method A:\nThreshold value is %s mm' % t1)
            print('A once in %s days driest day of %s:' % (input_frequency, city))
            for (k, v) in result1.items():
                print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')

        t2, result2 = get_exceptionally_low_values(len(df.index), input_frequency, date_set, df['rainfall'])  # Method B
        print('\nMethod B:\nThreshold value is %s mm' % t2)
        print('A once in %s days driest day of %s:' % (input_frequency, city))
        for (k, v) in result2.items():
            print('-'.join(str(x) for x in k), 'rainfall:', round(v, 1), 'mm')
