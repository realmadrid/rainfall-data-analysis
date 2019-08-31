1. Which file to run?
- Import the project from the root folder 'assignment' rather than python package 'assignment'
- Run in Anaconda3 python distribution
- main.py is the entry of the program

2. How to provide the necessary inputs?
- After running main.py, user will be guided by help messages to interact with the program:
(a) Please enter the path to the data file:
(b) Select the type of time series aggregation:
    1 - The total for each month.
    2 - The total for a specific month of the year.
    3 - The total for each year.
    4 - Single day.
If input 2, turn to (c), otherwise turn to (d).
(c) Enter a specific month(1 ~ 12):
(d) Select whether to compute a threshold for exceptionally high or low values:
    1 - Compute a threshold for exceptionally high values.
    2 - Compute a threshold for exceptionally low values.
(e) Please enter the frequency F.

3. What the program can do?
The program can:
- Filter invalid data and validate the integrity of the csv file.
- Compute aggregation by month, year, for a specific month of the year, and extraction of daily observations.
- Print total running time of aggregation function.
- Output the message that the data in some years/months is incomplete so the total amount for these years/months cannot
  be computed.
- Output the threshold value for extremely high as well as extremely low values according to two different methods.
- Output dates/months/years at which the data equals or exceeds/is less than it.

4. How to read the output of the program?
- The output is in clear format and easy to read.

5. Limitations and assumptions.
- To print the city name correctly, the csv file name should in uniform format: Rainfall_<City Name>_<number>.csv
- If the data of a month loses one days's data, the data of the month will be discarded.
- If the data of a year loses more than 3 days' data, the data of the year will be discarded.
- If the data of the beginning/end of time series is incomplete, those years/months/dates will also be regarded as data
  gap instead of ignoring them.
  In other words, all the years appeared in the csv file will be included in aggregation for year, month, and
  specific month even though some data might be missing.
- Count the gaps when determining the distance between two entries.
- The invalid data will be discarded.
- When obtaining a series of daily observations the program use only those observations that are taken on a single day
  because we do not know exactly how much fell on each day, and all the other days will be regarded as gaps.
- Assume that user's input are integer numbers in required range.
- Assume that values of frequency F make sense for specified time series aggregation.
- Assume data that has not been quality assured is not necessarily wrong.
- Assume that no multi-day observation spans more than one month.
