from delete_not_relevant_data import delete_not_relevant_csv
from sort_by_date import sort_date
from flightduration import calculate_flight_duration
from fillingGaps import fill_missing_arrivals, fill_missing_departure, fill_round_trip, count_na
import pandas as pd
import os

folder = "Forlder to sort"

#Delete fiels that contains not enought lines or too much lines 
min_lines = 48   #less than once a month in 4 years
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    if delete_not_relevant_csv(path,min_lines):
        os.remove(path)
print("Files deleted")

#Sort all fligths by date and add flight duration column
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    sort_date(path)
    calculate_flight_duration(path)
print("Files sorted")

#Fills the missing airports 
acceptable_range_round_trip = 0.1 # +-10%
acceptable_range_missing = 0.1 # +-10%
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    df = pd.read_csv(path)
    blanks = 10000
    while (blanks - count_na(df,["departure","arrival"])) !=0 :
        blanks = count_na(df,["departure","arrival"])
        df = fill_round_trip(df,acceptable_range_round_trip)
        df = fill_missing_arrivals(df,acceptable_range_missing)
        df = fill_missing_departure(df,acceptable_range_missing)
    df.to_csv(path, index=False)
print("Files filled ")

    




