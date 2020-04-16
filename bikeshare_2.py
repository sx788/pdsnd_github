import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to select? Chicago, New York City, or Washington?\n").title()
        if city not in ('Chicago', 'New York City', 'Washington'):
            print('Sorry, please make sure your selection is valid.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich months would you like to select? Ranging from January until June, or \"all\" if no preference.\n").title()
        if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
            print("Sorry, please make sure your selection is valid.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day would you like to select? Ranging from Monday until Sunday, or \"all\" if no preference.\n").title()
        if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All'):
            print("Sorry, please make sure your selection is valid.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data into df
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert START_TIME column to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day and create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # create new df filtered by selected month
        df = df[df['Month'] == month]

    # filter by day if applicable
    if day != 'All':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print('Most common month is', common_month)

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print('Most common day is', common_day)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('Most common hour is', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print('Most commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip
    #comb = df.loc[:, 'Start Station':'End Station'].mode()[0:]
    #freq_trip = comb['Trip Duration'].count().max
    #print('\nMost frequent comb:', comb)
    popular_station = df.loc[:, 'Start Station':'End Station'].mode()[0:]
    popular_station_amt = df.groupby(["Start Station", "End Station"]).size().max()
    print('Most popular trip:\n', popular_station, '\n Driven:', popular_station_amt,'times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = sum(df['Trip Duration'])
    print('Total travel time:', total_time/86400, " Days")

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print('No gender data available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth:", earliest_year)
        print("\nMost recent year of birth:", recent_year)
        print("\nMost common year of birth:", common_year)
    else:
        print('No birth year data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    i = 0
    show_data = input('\nDo you want to see raw data?\n')
    while show_data.title() == 'Yes':
        print(df.iloc[i:i + 5])
        i += 5
        show_data = input(
            '\nWould you like to see five more lines of raw data?\n'
            )

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
