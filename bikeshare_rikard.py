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
    city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

    while not (city == 'new york city' or city == 'chicago' or city == 'washington'):
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('What month do you want to see data for (All, January, February, ... , June)? ').lower()

    while not (month == 'all' or month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june'):
        month = input('What month do you want to see data for (All, January, February, ... , June)? ').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which weekday do you want to see data for (All, Monday, Tuesday, ... ,Sunday)? ').lower()

    while not (day == 'all' or day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday'):
        day = input('Which weekday do you want to see data for (All, Monday, Tuesday, ... , Sunday)? ').lower()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # combination of start station and end station trip
    df['combination_start_and_end_station'] = df['Start Station'] + ' ,' + df['End Station']


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month is {}'.format(popular_month))

    # display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most popular weekday is {}'.format(popular_weekday))

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('Most popular start hour is: ' + str(popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station is: ' + str(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station is: ' + str(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_combination_stations = df['combination_start_and_end_station'].mode()[0]
    print('Most popular combination of stations is (start station, end station): ' + str(popular_combination_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = np.sum(df['Trip Duration'])
    print('Total travel time is: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = np.mean(df['Trip Duration'])
    print('Mean travel time is: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user type: ' + str(user_types))


    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Count of gender: ' + str(gender))



    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year: ' + str(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year: ' + str(most_recent_birth_year))

        popular_birth_year = df['Birth Year'].value_counts().idxmax()
        print('Most popular birth year: ' + str(popular_birth_year))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Asks if user wants to see data.

    Returns:
        5 rows of data at a time.
    """

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    start_loc = 0

    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc+5, df.columns != 'combination_start_and_end_station'])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()



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
