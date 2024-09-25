# Creates WCVP.csv from Distribution.csv and Names.csv
# From the Royal Botanical Gardens (https://sftp.kew.org/pub/data-repositories/WCVP/)

import pandas as pd

# Import datasets
df_names = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Tree Nativity and Families\Distribution.csv',
                       sep="|", header=0, quoting=3, encoding="utf-8", keep_default_na=False)
df_distribution = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Tree Nativity and Families\Names.csv',
                              sep="|", header=0, quoting=3, encoding="utf-8", keep_default_na=False)

# Merge the two DataFrames based on the 'plant_name_id' column
merged_df = pd.merge(df_names, df_distribution, on='plant_name_id', how='inner')

# Display the headers of the merged DataFrame
print(merged_df.columns)

# Reduce the dataset to Canadian locations
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

# Reduce columns
columns_to_keep = ['plant_name_id', 'taxon_rank', 'family', 'genus_hybrid', 'genus', 'species_hybrid', 'species', 'taxon_name', 'area_code_l3', 'introduced']
WCVP_df = filtered_df[columns_to_keep]
WCVP_df = WCVP_df.rename(columns={'area_code_l3': 'Province'})
WCVP_df = WCVP_df.rename(columns={'taxon_name': 'Botanical Name'})

# Pivot the data to create new columns for each Province
df_pivot = WCVP_df.pivot_table(index=['Botanical Name', 'family'], columns='Province', values='introduced', fill_value=0)

# Reset the index to make 'taxon_name' and 'family' regular columns
df_pivot.reset_index(inplace=True)

# Display the pivoted DataFrame columns
print(df_pivot.columns)

# Deal with blank (missing) species ID, then make all species names lowercase and trim spaces
df_pivot['Botanical Name'] = df_pivot['Botanical Name'].str.lower().str.strip()
df_pivot['Botanical Name'] = df_pivot['Botanical Name'].str.replace(" x ", " ", regex=False)
df_pivot['Botanical Name'] = df_pivot['Botanical Name'].str.replace("'", "", regex=False)
df_pivot['Botanical Name'] = df_pivot['Botanical Name'].str.replace("xxxx ", "", regex=False)

# Add spp. to genus-only identification
def add_spp_if_only_genus(name):
    if isinstance(name, str) and len(name.strip().split()) == 1:  # Trim spaces and check if there's only one word
        return name.strip() + " spp."  # Trim spaces and add spp.
    return name.strip()  # Trim spaces in any case
df_pivot.loc[:, 'Botanical Name'] = df_pivot['Botanical Name'].apply(add_spp_if_only_genus) # Apply the function to the 'Botanical Name' column

# Remove any incorrect letters
df_pivot['Botanical Name'] = df_pivot['Botanical Name'].str.replace("Ã—", "", regex=False)
df_pivot['Botanical Name'] = df_pivot['Botanical Name'].str.replace("Ã", "", regex=False)

# Save the pivoted DataFrame to a CSV file
df_pivot.to_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Tree Nativity and Families\Pivoted Family and Distribution Data.csv', index=False)
