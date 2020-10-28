import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington? ")
    while (city.lower() not in ['chicago', 'new york', 'washington']):
        city = input("Wrong choose, try again ['chicago', 'new york', 'washington'] : ")
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Which month? All, January, February, March, April, May, or June? ")
    while(month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']):
        month = input("Wrong choose, try again ['all', 'january', 'february', 'march', 'april', 'may', 'june'] : ")
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? ")
    while(day.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
        day = input("Wrong choose, try again ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']: ")

    print('-'*40)
    return city.lower() , month.lower() , day.lower()


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
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month: ", df['month'].mode()[0])

    # TO DO: display the most common day of week
    print("Most common day of week: ", df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common hour of day: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most common start station: ", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("Most common end station: ", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print("Most common trip from start to end: ", (df['Start Station'] +' >> '+ df['End Station']).mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: ", df["Trip Duration"].sum())

    # TO DO: display mean travel time
    print("Average travel time: ", df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of each user type: ", df['User Type'].value_counts())

    if(city != "washington"):
        # TO DO: Display counts of gender
        print("Counts of each gender: ", df['Gender'].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
        print("Earliest, Most recent, Most common year of birth: ", 
              df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0])
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    """
    Prompt the user if they want to see 5 lines of raw data, 
    display that data if the answer is 'yes', 
    and continue these prompts and displays until the user says 'no'.
    """
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
    start_loc = 0 
    df_rows_count = df.shape[0]
    while (view_data=="yes"):
        
        # check if stop location exceed the last row then set it to last row
        stop_loc = start_loc+5 if start_loc+5 < df_rows_count else df_rows_count
        print(df.iloc[start_loc:stop_loc])
        start_loc += 5
        
        # break if start_loc exceed dataframe rows count
        if start_loc >= df_rows_count :
            print('\nYou reached the end of data rows.')
            break
            
        view_data = input("Do you wish to continue?Enter yes or no: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
