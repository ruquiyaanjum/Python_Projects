#PYTHON CODE FOR READING A MULTIPLE FILES FROM LOCAL DIRECTORY 

import os
import csv

# Define the folder containing CSV files
folder_path = "/home/data"

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Iterate over each CSV file
for file_name in csv_files:
    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)

    # Open the CSV file for reading
    with open(file_path, 'r') as file:
        print(f"Contents of {file_name}:")
        
        # Create a CSV reader object
        reader = csv.reader(file)

        # Read and process each row of the file
        for row in reader:
            # Print each field in the row
            for field in row:
                print(field)

        print()  # Print an empty line to separate files
