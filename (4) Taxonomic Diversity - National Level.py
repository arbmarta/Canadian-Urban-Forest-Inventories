# This code is based on the work of Ma et al. (2020) (DOI: 10.1016/j.ufug.2020.126826)

import pandas as pd

## Import data
master_df = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\(2) Filtered Master Dataset.csv', low_memory=False)
introduced_trees_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Tree Nativity and Families\Pivoted Family and Distribution Data.csv', low_memory=False)
family_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Families Index.csv', low_memory=False)
location_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Location Index.csv', low_memory=False)
downtown_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Downtown Areas.csv', low_memory=False)
find_and_replace = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Find and Replace 2.csv', low_memory=False)

## Drop any rows where botanical name is blank or species ID is "missing"
master_df['Botanical Name'] = master_df['Botanical Name'].str.strip()
rows_before = master_df.shape[0]
master_df = master_df[(master_df['Botanical Name'] != 'missing')]
master_df = master_df[(master_df['Botanical Name'].notna()) & (master_df['Botanical Name'] != '')]
rows_after = master_df.shape[0]
print(f"Number of rows before: {rows_before}")
print(f"Number of rows after: {rows_after}")

## Merge and clean data
df = master_df.merge(location_index, how='left', on='City')
df['Species'] = df['Botanical Name'].str.split().str[:2].str.join(' ')
replace_dict = dict(zip(find_and_replace['Species'], find_and_replace['Fix']))
df['Species'] = df['Species'].replace(replace_dict)
df['Species'] = df['Species'].str.lower()
df['Species'] = df['Species'].replace(replace_dict) # Run a second time - do NOT remove this function
df['Species'] = df['Species'].str.lower()

# Deal with blank (missing) species ID, then make all species names lowercase and trim spaces
df['Species'] = df['Species'].replace('', pd.NA).fillna('missing')
df['Species'] = df['Species'].str.lower().str.strip()
df['Species'] = df['Species'].replace('', pd.NA).fillna('missing')

# Standardize cultivars and species
df['Species'] = df['Species'].str.replace(" x ", " ", regex=False)
df['Species'] = df['Species'].str.replace("'", "", regex=False)

# Remove any non-living trees
df = df[~df['Species'].isin(["missing", "private", "not known", "vacant"])]

# Function to split, check, and replace 'x' with 'spp.'
def process_species(species):
    words = species.split()[:2]  # Split and keep the first two words
    if len(words) > 1 and words[1] == 'x':  # If the second word is 'x'
        words[1] = 'spp.'  # Replace 'x' with 'spp.'
    return ' '.join(words)  # Join the words back together

# Apply the function to the 'Species' column
df['Species'] = df['Species'].apply(process_species)

# Print the result
unique_species = df['Species'].unique()

# Function to extract the genus
def get_genus(species):
    words = species.split()
    if words[0] == 'x' and len(words) > 1:
        return words[1]  # Take the second word if the first is 'x'
    return words[0]  # Otherwise, take the first word

# Apply the function to create the Genus column
df['Genus'] = df['Species'].apply(get_genus)

# Get Family
df = df.merge(family_index, how='left', on='Genus')

## NATIONAL OVERVIEW
## Report the number of unique species, genera, and families
unique_counts = df[['Family', 'Genus', 'Species']].nunique()
print(unique_counts)

## Report the proportion of the ten most common species, genera, and families
top_species = (df['Species'].value_counts(normalize=True) * 100).round(2).head(10)
top_genus = (df['Genus'].value_counts(normalize=True) * 100).round(2).head(10)
top_family = (df['Family'].value_counts(normalize=True) * 100).round(2).head(10)

print("Top 10 Species (with proportions):\n", top_species)
print("\nTop 10 Genus (with proportions):\n", top_genus)
print("\nTop 10 Family (with proportions):\n", top_family)

# Get the top taxa names from value_counts
top_species_names = top_species.index.tolist()
top_genus_names = top_genus.index.tolist()
top_family_names = top_family.index.tolist()


# Function to count unique cities for each taxon where it appears at least 100 times
def count_unique_cities_for_taxa_min_count(df, column, taxa_list, min_count=100):
    city_counts = {}
    for taxa in taxa_list:
        # Filter for the current taxon
        filtered_df = df[df[column] == taxa]

        # Group by 'City' and count the occurrences for each city
        city_counts_for_taxa = filtered_df.groupby('City').size()

        # Count how many cities have at least `min_count` occurrences
        cities_with_min_count = (city_counts_for_taxa >= min_count).sum()

        # Store the result
        city_counts[taxa] = cities_with_min_count
    return city_counts


# Count unique cities where species, genus, and family appear at least 100 times
species_city_counts = count_unique_cities_for_taxa_min_count(df, 'Species', top_species_names)
genus_city_counts = count_unique_cities_for_taxa_min_count(df, 'Genus', top_genus_names)
family_city_counts = count_unique_cities_for_taxa_min_count(df, 'Family', top_family_names)

# Print the results
print("Top 10 Species and the number of cities where they appear at least 100 times:")
for species, count in species_city_counts.items():
    print(f"{species}: {count} cities")

print("\nTop 10 Genus and the number of cities where they appear at least 100 times:")
for genus, count in genus_city_counts.items():
    print(f"{genus}: {count} cities")

print("\nTop 10 Family and the number of cities where they appear at least 100 times:")
for family, count in family_city_counts.items():
    print(f"{family}: {count} cities")

## Report the number of native trees
introduced_trees_index['Species'] = introduced_trees_index['Botanical Name'].str.split().str[:2].str.join(' ')
province_columns = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'Newfoundland', 'Labrador', 'Nova Scotia', 'New Brunswick', 'Prince Edward Island']
introduced_trees_collapsed = introduced_trees_index.groupby('Species')[province_columns].min().reset_index()

# Function to concatenate province names where value is 0
def concatenate_provinces(row):
    provinces = []

    for province in province_columns:
        if row[province] == 0:
            provinces.append(province)

    if not provinces:
            return "None"

    return ' '.join(provinces) # Join the provinces with a space

introduced_trees_collapsed['Province Nativity'] = introduced_trees_collapsed.apply(concatenate_provinces, axis=1) # Apply the function to create the new column 'Province Nativity'
introduced_trees_collapsed = introduced_trees_collapsed[['Species', 'Province Nativity']]  # Remove all columns except Species and Province Nativity
native_tree_df = df.merge(introduced_trees_collapsed, how='left', on='Species')

def check_nativity(row):
    if pd.isna(row['Province Nativity']):  # Check if 'Province Nativity' is NaN
        return 'M'  # Use 'M' for missing species (not found in dataset)
    province_nativity = str(row['Province Nativity'])  # Convert 'Province Nativity' to a string
    return 'N' if row['Province'] in province_nativity else 'I'  # Check if 'Province' is in the 'Province Nativity'

native_tree_df['Nativity'] = native_tree_df.apply(check_nativity, axis=1)

print(native_tree_df)

missing_species = native_tree_df[native_tree_df['Nativity'] == 'M']['Species'].unique()

# Print the unique species names with nativity M (missing)
print("Unique species where Nativity is 'M':")
for species in missing_species:
    print(species)

# Number of native trees across Canada
n_count = native_tree_df['Nativity'].value_counts().get('N', 0)
i_count = native_tree_df['Nativity'].value_counts().get('I', 0)
m_count = native_tree_df['Nativity'].value_counts().get('M', 0)  # Count of missing species
native_tree_df['Nativity'] = native_tree_df['Nativity'].replace('M', 'I')

proportion_n = n_count / (n_count + i_count)

print(f"Count of 'N': {n_count}")
print(f"Proportion of 'N': {proportion_n}")

# Proportion of each city inventory that is native trees
nativity_counts_by_city = native_tree_df.groupby('City')['Nativity'].value_counts().unstack(fill_value=0) # Group by 'City' and count the number of 'N' and total trees for each city
nativity_proportion_by_city = (nativity_counts_by_city['N'] / (nativity_counts_by_city['N'] + nativity_counts_by_city['I'])) * 100 # Calculate the proportion of native trees ('N' / (N + I))
nativity_proportion_by_city = nativity_proportion_by_city.round(2) # Round the proportions to two decimal places

print("Proportion of native trees for each city (in percentages):")
print(nativity_proportion_by_city)
