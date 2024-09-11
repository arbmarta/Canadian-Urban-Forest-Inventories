import pandas as pd

# Load the merged CSV file
merged_df = pd.read_csv("data/wd/merged_inventory.csv", low_memory=False)

# Remove Dead and Stump values in Botanical Name
initial_count = merged_df.shape[0]
merged_df["Botanical Name"] = merged_df["Botanical Name"].str.lower()
filtered_df = merged_df[~merged_df["Botanical Name"].isin(["dead", "stump", "shrub", "shrubs", "vine", "vines", "hedge"])]
final_count = filtered_df.shape[0]

# Clean the DBH column
filtered_df["DBH"] = pd.to_numeric(filtered_df["DBH"], errors='coerce')
filtered_df.loc[filtered_df["DBH"] > 350, "DBH"] = 0
filtered_df.loc[filtered_df["DBH"] == 0, "DBH"] = pd.NA
num_rows_with_dbh_0 = filtered_df[filtered_df["DBH"] == 0].shape[0]
print(f"Number of rows with DBH of 0: {num_rows_with_dbh_0}")

# Calculate basal area
filtered_df['Basal Area'] = 0.00007854 * (filtered_df['DBH'] ** 2)

# Remove rows where both DAUID and CTUID are missing
filtered_df = filtered_df[~(filtered_df["DAUID"].isna() & filtered_df["CTUID"].isna())]

# Count the number of rows after removing rows with missing DAUID and CTUID
final_count_after_missing_removal = filtered_df.shape[0]

# Find and count unique values of DAUID where CTUID is blank
blank_ctuid_df = filtered_df[filtered_df["CTUID"].isna()]
unique_dauid_with_blank_ctuid = blank_ctuid_df["DAUID"].unique()
num_instances_blank_ctuid = blank_ctuid_df.shape[0]

print("Unique DAUID values where CTUID is blank:")
print(unique_dauid_with_blank_ctuid)
print(f"Number of instances where CTUID is blank: {num_instances_blank_ctuid}")

# Fill missing CTUID values
data_dict = {
    'DAUID': [59150883, 59150891, 59153562, 59170272, 35240431, 35100286, 35201466, 35204675, 35204821, 35205067,
              35370553, 24580007, 24662985, 24662707, 24662951, 24662821, 24662885, 24660984, 24663395, 24230066,
              13100304, 13070131, 12090576, 59154073],
    'CTUID': [9330045.01, 9330025, 9330059.08, 9350001, 5370204, 5210100.01, 5350003, 5350210.04, 5350012.01, 5350200.01,
              5590043.02, 4620886.03, 4620288, 4620276, 4620585.01, 4620290.05, 4620290.09, 4620322.03, 4620390, 4210310,
              3200009, 3050006, 2050112, 9330202.01],
    'City': ['Vancouver', 'Vancouver', 'Vancouver', 'Victoria', 'Burlington', 'Kingston', 'Toronto', 'Toronto', 'Toronto', 'Toronto',
             'Windsor', 'Longueuil', 'Montreal', 'Montreal', 'Montreal', 'Montreal', 'Montreal', 'Montreal', 'Montreal', 'Quebec City',
             'Fredericton', 'Moncton', 'Halifax', 'New Westminster']
}

data_dict_df = pd.DataFrame(data_dict)

# Merge the filtered DataFrame with the data dictionary DataFrame based on "DAUID"
filtered_df = filtered_df.merge(data_dict_df, on='DAUID', how='left', suffixes=('', '_dict'))

# Fill missing CTUID and City values from the dictionary
filtered_df['CTUID'] = filtered_df['CTUID'].combine_first(filtered_df['CTUID_dict'])
filtered_df['City'] = filtered_df['City'].combine_first(filtered_df['City_dict'])

# Drop the extra columns from the dictionary
filtered_df = filtered_df.drop(columns=['CTUID_dict', 'City_dict'])
print("CTUID and City columns updated based on DAUID.")

# Count the number of instances of DAUID with blank CTUID after filling
blank_ctuid_df_after_filling = filtered_df[filtered_df["CTUID"].isna()]
num_instances_blank_ctuid_after_filling = blank_ctuid_df_after_filling.shape[0]

# Save the updated DataFrame to the master CSV file
filtered_df.to_csv("data/wd/cleaned_master.csv", index=False)

# Print the counts
print(f"Number of trees where CTUID is blank after filling: {num_instances_blank_ctuid_after_filling}")
print(f"Number of trees after removing trees with missing DAUID and CTUID: {final_count_after_missing_removal}")
print(f"Number of out-of-city trees removed: {final_count - final_count_after_missing_removal}")
print(f"Number of dead trees and stumps removed: {initial_count - final_count}")
print("Filtered and cleaned data saved to cleaned_master.csv.")
