from delete_not_relevant_data import delete_not_relevant_csv
from sort_by_date import sort_date
from flightduration import calculate_flight_duration
from fillingGaps import (fill_missing_arrivals, fill_missing_departure, fill_round_trip
                        ,count_na_airports, delete_too_much_blanks, fill_with_unknown,
                        delete_if_unknown)
import pandas as pd
import os

folder = "Folder to sort"

#Delete fiels that contains not enought lines or too much lines 
min_lines = 48   #less than once a month in 4 years
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    if delete_not_relevant_csv(path,min_lines):
        os.remove(path)


#Sort all fligths by date and add flight duration column
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    sort_date(path)
    calculate_flight_duration(path)


#Fills the missing airports 
acceptable_range_round_trip = 0.1 # +-10%
acceptable_range_missing = 0.1 # +-10%
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    df = pd.read_csv(path)
    blanks = 10000
    while (blanks - count_na_airports(df,["departure","arrival"])[0]) !=0 :
        blanks = count_na_airports(df,["departure","arrival"])[0]
        df = fill_round_trip(df,acceptable_range_round_trip)
        df = fill_missing_arrivals(df,acceptable_range_missing)
        df = fill_missing_departure(df,acceptable_range_missing)
    df.to_csv(path, index=False)

#Delete files if the ratio blank lines/total lines is over 'acceptable_range_blank_lines'
#Or delete blank lines if the ration is lower then the acceptable range
acceptable_range_blank_lines = 4
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    df = pd.read_csv(path)
    result, output, percentage1, percentage2 = delete_too_much_blanks(df,acceptable_range_blank_lines)
    if result == True:
        print(f"{file} deleted, {output}% unsuable data: {percentage1}% missing both airports &  {percentage1}% missing flight duration ")
        os.remove(path)
    else:
        output.to_csv(path, index=False)

acceptable_range_blank_airport = 15
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    df = pd.read_csv(path)
    total_na, _, _ = count_na_airports(df)
    print(total_na)
    percentage = round(total_na/len(df)*100,1)
    if  percentage> acceptable_range_blank_airport:
         print(f"{file} deleted, too much unknown airports : {percentage}")
         os.remove(path)
    print(f"{file}: {percentage}%")

#Filling remaining blanks with 'unknown departure' et 'unknown arrival'
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    df = pd.read_csv(path)
    df = fill_with_unknown(df)  #I know it doesn't make any sense, but I'm deleting the unknowns 
    df = delete_if_unknown(df)  #until I figure out how to handle them differently
    df.to_csv(path, index=False)




