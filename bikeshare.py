import time
import pandas as pd
import numpy as np



def load_data (filename, filtro, param):
    """ Description: Load particular city and filter data if user want to do so 
        Return a dataframe with filters or not filtered
    """
    df = pd.read_csv(filename)
    
    df = convert_str_to_date(df)
   
    if filtro > 0:
        if filtro == 1:
            df = df[df['Start Time weekday'] == param]
        if filtro == 2:    
            df = df[df['Start Time month'] == param]
        if filtro == 3:
            df = df[df['Start Time year'] == param]
        return df   
    else:
        return df

def describe_df (df,city):
    """ Description: Describe dataframe to know columns and datatypes 
        No return value
    """
    df_cols = df.columns
    df_desc = df.describe
    #df_rows = df[0].value_counts()
    print ("\nColumns of " + city + " dataframe : \n")
    print (df_cols)
    
def convert_str_to_date(df):
    """ Description: Convert string values to datetime and create new columns with information about
    the travel information (hour, month, day, etc).
        Return a dataframe with the new created values
    """    
    
    df['Start Time hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['Start Time month'] = pd.to_datetime(df['Start Time']).dt.month
    df['Start Time day'] = pd.to_datetime(df['Start Time']).dt.day
    df['Start Time year'] = pd.to_datetime(df['Start Time']).dt.year
    df['Start Time weekday'] = pd.to_datetime(df['Start Time']).dt.day_name()
    
    
    return df
    
def gral_stats(df, city):
    
    """ Description: Generate and show general stats about the dataframe
        Return no value
    """
    
    popular_hour        = df['Start Time hour'].mode()[0]
    popular_month       = df['Start Time month'].mode()[0]
    popular_day         = df['Start Time weekday'].mode()[0]
    
    popular_str_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    
    total_travel_time   = df['Trip Duration'].sum()
    avg_travel_time     = df['Trip Duration'].mean()
    
    df["Combination"]   = df['Start Station'] + ' to ' + df['End Station'] 
    popular_combination = df["Combination"].mode()[0]
    
    print ("The most popular start hour is {}\n".format(popular_hour))
    print ("The most popular start month is {}\n".format(MONTHS[popular_month]))
    print ("The most popular start day is {}\n".format(popular_day))
    
    print ("The most popular start station is {}\n".format(popular_str_station))
    print ("The most popular end station is {}\n".format(popular_end_station))
    print ("The total travel time is: {} \n".format(total_travel_time))
    print ("The average travel time is: {} \n".format(avg_travel_time))
    print ("The most popular combination is: {} \n".format(popular_combination))
    
    if city in ['Chicago','New York']:
        gender_counts       = df["Gender"].value_counts()
        
        popular_year_birth  = int(df["Birth Year"].mode()[0])
        earliest_year_birth = int(df["Birth Year"].min())
        recent_year_birth   = int(df["Birth Year"].max())
        
        print (gender_counts)
        print ("The most common year of birth is: {} \n".format(popular_year_birth))
        print ("The most earliest year of birth is: {} \n".format(earliest_year_birth))
        print ("The most recent year of birth is: {} \n".format(recent_year_birth))
    
    
def users_breakdown(df):
    
    """ Description: Generate value counts for user types and show it on screen
        Return no value
    """
    
    user_types = df['User Type'].value_counts()
    print (user_types)
    
def view_rows(df,n_rows):
    
    """ Description: slice dataframe to show it on screen
        Return verify variable to break the while loop or continue
    """    
    
    start_row = n_rows - 5
    #n_rows += 1
    
    df = df.iloc[start_row:n_rows,1:]
    print (df)
    
    verify = input("\n Do you want to display the next 5 rows? (yes no): \t")
    
    return verify    
   

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

CITIES = ['Chicago','New York', 'Washington']
CITIES_OPT = ['1','2','3']

MONTHS = ['','January', 'February', 'March', 'April', 'May', 'June']

DAYS = ['','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

SELECT_OPTIONS = ["yes", "no"]

VERIFY_TEXT = '\nThe option is not valid. Please verify your answer '

def main():
    
    data_city = {}

    while True:
        
        """ It will iterate until user choose to cancel """
    
        print (".:: Welcome to bikeshare analytics information ::.\n")
        print ("-> The following cities are available: \n")
        
        print ("\n [1] Chicago \n [2] New York \n [3] Washington\n")
        
        temp = input("What city you want to view?\t")
        city_selected = temp
        
        while True:
        
            if city_selected in CITIES_OPT:
                city_selected = int(temp) - 1
                print ("You have selected {}".format(CITIES[city_selected]))
                break
            else:
                print(VERIFY_TEXT)
                temp = input("\nWhat city you want to view?\t")
                city_selected = temp 
            
        print("\nYou may filter the dataset by day, month, year\n")
        print("\n[0] None \n[1] Day\n[2] Month\n")
        
        filtro  = input ("Specify a filter do you want to apply on data: \t")
                
        """ Build the user menu associated with the filter type and capture the 
            parameters to filter the data 
        """
        
        while True:
            
            if filtro in ['0','1','2']:
                
                filtro_int = int(filtro)
        
                if filtro_int == 0:
                    param = 0
                    break
                
                if filtro_int == 1:
                    aux = 0
                    for value in range(1,8):
                        aux += 1
                        day = DAYS[value]
                        print ("[" + str(aux) + "]" + day + "\n")
                    param = input("\n Which value?:\t")
                    
                    while True:
                        if param in     ['1','2','3','4','5','6','7']:
                            param = int(param)
                            param = DAYS[param]
                            param_valid = 1
                            break
                        else:
                            print(VERIFY_TEXT)
                            param = input("\n Which value?:\t")
                        
                if filtro_int == 2:
                    aux = 0
                    for value in range(1,7):
                        aux += 1
                        month = MONTHS[value]
                        print ("[" + str(aux) + "]" + month + "\n")      
                    param = input("\n Which value?:\t")
                    
                    while True:
                        if param in ['1','2','3','4','5','6']:
                            param = int(param)
                            param_valid = 1
                            break
                        else:
                            print(VERIFY_TEXT)
                            param = input("\n Which value?:\t")
                
                if param_valid == 1:
                    break
                
            else:
                print(VERIFY_TEXT)
                filtro  = input ("\nSpecify a filter do you want to apply on data: \t")
        
        print ("\nWe're proccesing the data for you now, please wait a moment...\n")
            
        for city in CITY_DATA.items():
            
            if CITIES[city_selected] == city[0]:
            
                filename = city[1]
                data_city = load_data(filename,filtro_int, param)
                          
                data_city = convert_str_to_date(data_city)
                
                print("\nInformation for " + city[0] + ": \n")
                
                describe_df (data_city, city[0])
                gral_stats(data_city, city[0])
                #sers_breakdown(data_city)
                
                verify = "yes"
                n_rows = 5
                
                print ("\nHere is some rows of the dataset")
                
                while True:
                    
                    if verify in SELECT_OPTIONS:
                        if verify.lower() == "yes":
                            verify = view_rows(data_city,int(n_rows))
                            n_rows += 5
                        else:
                            break
                    else:
                        print("\nThe option is not valid. Please verify your answer")
                        verify = input("\nDo you want to display the next 5 rows?  (yes no): \t")
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        

        if restart in SELECT_OPTIONS:
            if restart.lower() != 'yes':
                print ("--" * 40)
                print("\n.:: Thank you for using the Bikeshare Analytics software. Have a nice day ::.")
                break
            else:
                continue
        else:
             print("\nThe option is not valid. Please verify your answer")
             restart = input("\nWould you like to restart? Enter yes or no.\n")

if __name__ == "__main__":
	main()
