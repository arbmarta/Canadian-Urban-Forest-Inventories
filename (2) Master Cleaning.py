import pandas as pd
import re

# Load the merged CSV file
merged_df = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\(1) Master Dataset.csv', low_memory=False)
species_clean_df = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Find and Replace.csv', low_memory=False)

## Clean the Botanical Name column
initial_count = merged_df.shape[0]

# Deal with blank (missing) species ID, then make all species names lowercase and trim spaces
merged_df['Botanical Name'] = merged_df['Botanical Name'].replace('', pd.NA).fillna('missing')
merged_df['Botanical Name'] = merged_df['Botanical Name'].str.lower().str.strip()
merged_df['Botanical Name'] = merged_df['Botanical Name'].replace('', pd.NA).fillna('missing')

# Standardize cultivars and species
merged_df['Botanical Name'] = merged_df['Botanical Name'].str.replace(" x ", " ", regex=False)
merged_df['Botanical Name'] = merged_df['Botanical Name'].str.replace("'", "", regex=False)

# Use find and replace to deal with spelling mistakes in inventory datasets
for index, row in species_clean_df.iterrows():
    find = row['Find']
    replace = row['Replace']

    # Ensure word boundaries are respected in the replacement to avoid partial replacements
    pattern = r'\b' + re.escape(find) + r'\b'

    merged_df['Botanical Name'] = merged_df['Botanical Name'].str.replace(pattern, replace, regex=True)

# Remove any non-living trees
filtered_df = merged_df[~merged_df["Botanical Name"].isin(["dead", "stump", "stump spp.", "stump for", "shrub", "shrubs", "vine", "vines", "hedge", "vacant"])]

# Add spp. to genus-only identification
def add_spp_if_only_genus(name):
    if isinstance(name, str) and len(name.strip().split()) == 1:  # Trim spaces and check if there's only one word
        return name.strip() + " spp."  # Trim spaces and add spp.
    return name.strip()  # Trim spaces in any case
filtered_df.loc[:, 'Botanical Name'] = filtered_df['Botanical Name'].apply(add_spp_if_only_genus) # Apply the function to the 'Botanical Name' column
final_count = filtered_df.shape[0]

# Remove any incorrect letters
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("Ã—", "", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("Ã", "", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("_x000d_", "", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("â€˜", "", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("â€™", "", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace(" '", " ", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace(" x ", " ", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("'", "", regex=False)

# Spot check functions
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("pinus missing", "pinus spp.", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("stump spp.", "missing", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("malus sp.", "malus spp.", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("..", ".", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("magnolia missing", "magnolia spp.", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("missing.", "missing", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("missing spp.", "missing", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("pyrus missing", "pyrus spp.", regex=False)
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("malus missing", "missing", regex=False)

# Ensure any non-living trees are removed
filtered_df['Botanical Name'] = filtered_df['Botanical Name'].str.replace("spp. spp.", "missing", regex=False)

# Save the updated DataFrame to the master CSV file
filtered_df.to_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\(2) Filtered Master Dataset.csv', index=False)
print("Filtered Master Dataset file created successfully.")
