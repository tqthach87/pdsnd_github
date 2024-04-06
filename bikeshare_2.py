import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def ask_for_input(question, valid_answers):
    """
    Asks a user to input a specified value

    Args:
        (str) question - a question string
        (list) valid_answers - a list of valid answers
    Returns:
        (str) input value - the valid value of the input
    """
    still_input = True
    inp = ''

    while still_input:
        inp = input(f'{question} : ')

        # lower all inputted strings
        inp = inp.lower()

        if inp in valid_answers:
            # the inputted data matching one of items list
            still_input = False
        else:
            print('Your input is an invalid value. Please try again!')
        
    return inp


def find_most_popular(ds):
    """
    Find the most popular of data serie

    Args:
        (ds) data serie wants to find the most popular
    Returns:
        most_popular_value: the most popular value based on inputted data serie
        count_most_popular_value = count of the most popular value    
    """
    most_popular_value = ds.mode()[0]
    count_most_popular_value = ds.value_counts().values[0]
    
    return most_popular_value, count_most_popular_value


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # set some default value
    city = 'chicago'
    month = 'all'
    day = 'all'

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    question_1 = 'Would you like see data for Chicago, New York City, or Washington?'
    city = ask_for_input(question_1, CITY_DATA)

    question_2 = 'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.'
    data_filter = ask_for_input(question_2, ['month', 'day', 'both', 'none'])
    
    if data_filter == 'none':
        month = 'all'
        day = 'all'
    else:
        # get user input for month (all, january, february, ... , june)
        if data_filter == 'both' or data_filter == 'month':
            question_3 = 'Which month? all, January, February, March, April, May, or June?'
            month = ask_for_input(question_3, ['all', 'january', 'february', 'march', 'april', 'may', 'june'])

        # get user input for day of week (all, monday, tuesday, ... sunday)
        if data_filter == 'both' or data_filter == 'day':
            question_4 = 'Which day? Please type your response as an integer (e.g., 1=Sunday) or all'
            day_of_week = {'all': 'all', '1': 'sunday', '2': 'Monday', '3': 'Tuesday', '4': 'Wednesday', '5': 'Thursday', '6': 'Friday', '7': 'Saturday'}
            day_dict_key = ask_for_input(question_4, day_of_week)
            day = day_of_week[day_dict_key]

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    popular_month, count_popular_month = find_most_popular(df['month'])
    print('Most Popular Start Month:', popular_month, '. Count:', count_popular_month)    

    # display the most common day of week
    popular_day_of_week, count_popular_day_of_week = find_most_popular(df['day_of_week'])
    print ('Most Popular Start Day of Week:', popular_day_of_week, '. Count:', count_popular_day_of_week)

    # display the most common start hour
    ## convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    ## extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    ## find the most popular hour
    popular_hour, count_popular_hour = find_most_popular(df['hour'])
    
    print('Most Popular Start Hour:', popular_hour, '. Count:', count_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station, count_popular_start_station = find_most_popular(df['Start Station'])
    
    print('Most Popular Start Station:', popular_start_station, '. Count:', count_popular_start_station)

    # display most commonly used end station
    popular_end_station, count_popular_end_station = find_most_popular(df['End Station'])
    
    print('Most Popular End Station:', popular_end_station, '. Count:', count_popular_end_station)

    # display most frequent combination of start station and end station trip
    df['combine_start_station_end_station'] = df['Start Station'] + " to " + df['End Station']
    popular_combination, count_popular_combination = find_most_popular(df['combine_start_station_end_station'])
    
    print("The most frequent combination of start station and end station trip: ", popular_combination, ". Count: ", count_popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df['Trip Duration'].sum()) / (60 * 60)
    
    print("Total travel time:", total_travel_time, "hr(s)")

    # display mean travel time
    mean_travel_time = (df['Trip Duration'].mean()) / (60)
    
    print("Mean travel time:", mean_travel_time, "min")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    dict_count_user_types = count_user_types.to_dict()
    
    print('Counts of user types:')
    for key, value in dict_count_user_types.items():
        print('+', key,":", value)
        
    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        dict_count_gender = count_gender.to_dict()
    
        print('Counts of user types:')
        for key, value in dict_count_gender.items():
            print('+', key,":", value)
    except (KeyError):
        print('Thero no Gender column. Skip this statistics')
              
    # Display earliest, most recent, and most common year of birth
    try:
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mode()[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except (KeyError):
        print('Thero no Birth Year column. Skip this statistics')


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        
        #if there is no data, not process any more
        if df['month'].count() != 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print('There is no data for our input')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
