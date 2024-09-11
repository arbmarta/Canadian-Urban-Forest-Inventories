import os
from pathlib import Path

import pandas as pd

# All datasets have, in order, Botanical Name, DBH, DAUID, CTUID, and City.

cities = ["Kelowna", "Maple Ridge", "New Westminster", "Vancouver", "Victoria", "Calgary", "Edmonton", "Lethbridge",
          "Strathcona County", "Regina", "Winnipeg", "Ajax", "Burlington", "Guelph", "Kingston", "Kitchener",
          "Mississauga", "Niagara Falls", "Ottawa", "Peterborough", "St. Catherines", "Toronto", "Waterloo", "Welland",
          "Whitby", "Windsor", "Longueuil", "Montreal", "Quebec City", "Fredericton", "Moncton", "Halifax"]

# Initialize an empty list to hold the data
data_frames = []

# Process each city file
for city in cities:
    file_name = f"data/cities/{city}.xlsx"

    # Check if the file exists
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)

        # Append the DataFrame to the list
        data_frames.append(df)
    else:
        print(f"{city} file does not exist.")

if len(data_frames) <= 0:
    raise ValueError("No cities XLSX files loaded... Ensure they have been placed in data/cities subdir.")

# Concatenate all DataFrames
master_df = pd.concat(data_frames, ignore_index=True)

# Convert inches to cm in Vancouver
master_df.loc[master_df['City'] == 'Vancouver', 'DBH'] *= 2.54

## Species codes to scientific binomials


Path("data/wd").mkdir(exist_ok=True)

# Save the master DataFrame to a CSV file
master_df.to_csv("data/wd/merged_inventory.csv", index=False)

print("Merged CSV file created successfully.")
