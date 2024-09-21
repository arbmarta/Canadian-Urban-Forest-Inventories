# Creates WCVP.csv from Distribution.csv and Names.csv
# From the Royal Botanical Gardens (https://sftp.kew.org/pub/data-repositories/WCVP/)

import pandas as pd

# Import datasets
df_names = pd.read_csv(r'{file_path}\Distribution.csv',
                       sep="|", header=0, quoting=3, encoding="utf-8", keep_default_na=False)
df_distribution = pd.read_csv(r'{file_path}\Names.csv', sep="|", header=0, quoting=3, encoding="utf-8",
                              keep_default_na=False)

# Merge the two DataFrames based on the 'plant_name_id' column
merged_df = pd.merge(df_names, df_distribution, on='plant_name_id', how='inner')

# Display the headers of the merged DataFrame
print(merged_df.columns)

#  Reduce the dataset to Canadian locations
provincial_codes = ['MAN', 'ONT', 'SAS', 'ABT', 'BRC', 'QUE', 'PEI', 'NBR', 'NSC', 'NFL', 'LAB']
filtered_df = merged_df[merged_df['area_code_l3'].isin(provincial_codes)]

## Area Code Level 3: Three letter botanical area code (TDWG Level 3)
# Manitoba : MAN
# Ontario : ONT
# Saskatchewan : SAS
# Alberta : ABT
# British Columbia : BRC
# Quebec : QUE
# Prince Edward Island : PEI
# New Brunswick : NBR
# Nova Scotia : NSC
# Newfoundland : NFL
# Labrador : LAB

# reduce columns
columns_to_keep = ['plant_name_id', 'taxon_rank', 'family', 'genus_hybrid', 'genus', 'species_hybrid', 'species', 'taxon_name', 'area_code_l3', 'introduced', 'extinct']
WCVP_df = filtered_df[columns_to_keep]

# Display the filtered DataFrame
print(WCVP_df.columns)
WCVP_df.to_csv(r'{file_path}\WCVP.csv', index=False)
