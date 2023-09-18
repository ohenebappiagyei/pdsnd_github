import pandas as pd
import time

# Define the city data filenames
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Get user input for city, month, and day of the week.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        # Get user input for city
        city = input('Enter the city (Chicago, New York City, Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city. Please enter a valid city name.')

    while True:
        # Ask the user if they want to filter by month, day, both, or none
        filter_choice = input('Would you like to filter the data by month, day, both, or none? Enter "month", "day", "both", or "none": ').lower()
        if filter_choice in ('month', 'day', 'both', 'none'):
            break
        else:
            print('Invalid choice. Please enter "month", "day", "both", or "none".')

    if filter_choice == 'none':
        return (city, 'All', 'All')
    else:
        month = 'All' if filter_choice in ('day', 'none') else get_month_input()
        day = 'All' if filter_choice in ('month', 'none') else get_day_input()
        return (city, month, day)

def get_month_input():
    """
    Get user input for the month filter.
    """
    while True:
        month = input('Enter the month (January, February, ..., June): ').title()
        if month in ('January', 'February', 'March', 'April', 'May', 'June'):
            return month
        else:
            print('Invalid month. Please enter a valid month.')

def get_day_input():
    """
    Get user input for the day filter.
    """
    while True:
        day = input('Enter the day of the week (Monday, Tuesday, ..., Sunday): ').title()
        if day in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            return (day)
        else:
            print('Invalid day of the week. Please enter a valid day.')

def load_data(city, month, day):
    """
    Load and filter the dataset for the specified city, month, and day.
    """
    # Load the dataset for the specified city
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    
    # Convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of the week
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    
    # Apply month filter
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month_num = months.index(month) + 1
        df = df[df['Month'] == month_num]
    
    # Apply day filter
    if day != 'All':
        df = df[df['Day of Week'] == day]
    
    return (df)

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    common_month = df['Month'].mode()[0]
    print(f'The most common month is: {common_month}')

    # Most common day of the week
    common_day = df['Day of Week'].mode()[0]
    print(f'The most common day of the week is: {common_day}')

    # Most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f'The most common start hour is: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f'The most commonly used start station is: {common_start_station}')

    # Most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f'The most commonly used end station is: {common_end_station}')

    # Most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f'The most frequent combination of start station and end station trip is: {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total travel time (in seconds): {total_travel_time}')

    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean travel time (in seconds): {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_types)

    # Display counts of gender if available
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of gender:')
        print(gender_counts)
    else:
        print('\nGender information not available for this city.')

    # Display earliest, most recent, and most common year of birth if available
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('\nBirth Year Statistics:')
        print(f'Earliest Birth Year: {earliest_birth_year}')
        print(f'Most Recent Birth Year: {most_recent_birth_year}')
        print(f'Most Common Birth Year: {common_birth_year}')
    else:
        print('\nBirth Year information not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    """
    Display raw data in batches of 5 rows at a time based on user input.
    """
    start_index = 0
    end_index = 5
    while True:
        raw_data = df.iloc[start_index:end_index]
        print(raw_data)
        start_index += 5
        end_index += 5
        more_data = input('\nWould you like to see 5 more rows of raw data? Enter yes or no.\n')
        if more_data.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
