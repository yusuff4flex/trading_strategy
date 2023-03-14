import datetime
from suntime import Sun
from geopy.geocoders import Nominatim
import calendar
import numpy as np
from nltk import flatten
import pandas as pd
from pytz import timezone

def get_sunset_time(start_year):
    start_month = 1
    cal = calendar.Calendar()

    # Initialise output lists
    dates = []
    sunrises = []
    sunsets = []

    # Iterate over four months
    for i in range(18):
        month = start_month + i
        # If you overflow the year, move to the next year
        year = int(start_year + np.floor((month - 1) / 12))
        # Similarly correct the month
        month = month % 12
        if month == 0:
            month = 12
        # For each day in that month in that year
        for day in cal.itermonthdates(year, month):
            if day.month == month:
                day_datetime = datetime.datetime(day.year, day.month, day.day)
                dates.append(day.strftime('%Y-%m-%d'))
    Time = []
    dates_of_the_month = []
    for month in range(1, 13):
        time = []
        days = []
        for day in range(1, 32):
            if month == 2 and day > 28:
                continue
            if month in [4, 6, 9, 11] and day > 30:
                continue
            date = datetime.date(start_year, month, day)

    # Nominatim API to get latitude and longitude
            geolocator = Nominatim(user_agent="geoapiExercises")

            # input place
            place = "Hannover"
            location = geolocator.geocode(place)

            # latitude and longitude fetch
            latitude = location.latitude
            longitude = location.longitude
            sun = Sun(latitude, longitude)

            # date in your machine's local time zone
            time_zone = datetime.date(start_year, month, day)
            #print(time_zone)
            sun_rise = sun.get_local_sunrise_time(time_zone)
            sun_dusk = sun.get_local_sunset_time(time_zone)
            start_time = (sun_dusk- datetime.timedelta(hours=1)).time()
            #print(start_time)
            time.append(start_time)
        Time.append(time)
    liste = list(flatten(Time))
    print(liste)
    # Add 1 minute to the current time
        # current_time = (datetime.datetime.combine(date, current_time) + datetime.timedelta(minutes=1)).time()
    df = pd.read_csv('20230216_Price and renewables_2018-2023_incomplete.csv')

    # df['datetime'] = pd.DataFrame({'datetime': pd.date_range(start=start, end=end, freq='15min', closed='left')})
    df['time'] = pd.to_datetime(df['time'])
    df = df[df['time'].dt.year == start_year]

        # sunset_times = [datetime.time(15, 5), datetime.time(15, 7), datetime.time(15, 8), datetime.time(15, 9)]

        # Start date
    start_date = datetime.date(start_year, 1, 1)

        # Loop through each day in the list of sunset times
    for i, sunset_time in enumerate(liste):
            # Create datetime objects for the sunset time and 23:45:00 of the current day
        current_date = start_date + datetime.timedelta(days=i)
        sunset_datetime = datetime.datetime.combine(current_date, sunset_time)
        end_of_day_datetime = datetime.datetime.combine(current_date, datetime.time(23, 45))
            # Find rows where the datetime is between the sunset time and 23:45:00 of the current day and fill the new column with 1s
        df.loc[(df['time'] >= sunset_datetime) & (df['time'] <= end_of_day_datetime), 'new_col'] = 1

    return df

year_2022_sunset = get_sunset_time(2022)
year_2021_sunset = get_sunset_time(2021)
combined_dataframe = pd.concat([year_2021_sunset, year_2022_sunset]).drop_duplicates()
combined_dataframe.to_csv('trading_strategy_2022.csv')
print(year_2022_sunset)

