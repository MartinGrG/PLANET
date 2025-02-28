import os
import csv

# Specify the folder path
def delete_not_relevant_csv(input_file, minimum):
        # Check if the input file is a CSV file
        if input_file.endswith(".csv"):
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Check if the file has fewer lines than the minimum
                if (len(lines) < minimum):
                    return True
