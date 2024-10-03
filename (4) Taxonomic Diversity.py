# This code is based on the work of Ma et al. (2020) (DOI: 10.1016/j.ufug.2020.126826)

import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu

## Import data
master_df = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\(2) Filtered Master Dataset.csv', low_memory=False)
introduced_trees_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Tree Nativity and Families\Pivoted Family and Distribution Data.csv', low_memory=False)
family_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Families Index.csv', low_memory=False)
location_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Location Index.csv', low_memory=False)
downtown_index = pd.read_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\Non-Inventory Datasets\Downtown Areas.csv', low_memory=False)

## Drop any rows where botanical name is blank or species ID is "missing"
master_df['Botanical Name'] = master_df['Botanical Name'].str.strip()
rows_before = master_df.shape[0]
master_df = master_df[(master_df['Botanical Name'] != 'missing')]
master_df = master_df[(master_df['Botanical Name'].notna()) & (master_df['Botanical Name'] != '')]
rows_after = master_df.shape[0]
print(f"Number of rows before: {rows_before}")
print(f"Number of rows after: {rows_after}")

## Merge data
df = master_df.merge(location_index, how='left', on='City')
df['Genus'] = df['Botanical Name'].str.split().str[0]
df['Species'] = df['Botanical Name'].str.split().str[:2].str.join(' ')
df = df.merge(family_index, how='left', on='Genus')

## Report the number of unique species, genera, and families
unique_counts = df[['Family', 'Genus', 'Species']].nunique()
print(unique_counts)

## Report the proportion of the six most common species, genera, and families
top_species = df['Species'].value_counts(normalize=True).head(6)
top_genus = df['Genus'].value_counts(normalize=True).head(6)
top_family = df['Family'].value_counts(normalize=True).head(6)

print("Top 6 Species (with proportions):\n", top_species)
print("\nTop 6 Genus (with proportions):\n", top_genus)
print("\nTop 6 Family (with proportions):\n", top_family)

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
print(native_tree_df.columns)

print(native_tree_df['City'].unique())


def check_nativity(row):
    if pd.isna(row['Province Nativity']): # Check if 'Province Nativity' is NaN
        return 'I'  # Introduced if 'Province Nativity' is NaN
    province_nativity = str(row['Province Nativity']) # Convert 'Province Nativity' to a string to safely check for province
    return 'N' if row['Province'] in province_nativity else 'I' # Check if 'Province' is in the 'Province Nativity' string

native_tree_df['Nativity'] = native_tree_df.apply(check_nativity, axis=1)

print(native_tree_df)

nativity_counts = native_tree_df['Nativity'].value_counts()
n_count = nativity_counts.get('N', 0)
total_count = n_count + nativity_counts.get('I', 0)
proportion_n = n_count / total_count if total_count > 0 else 0
proportion_n

## Calculate Shannon Wiener Index for each city
def shannon_wiener_index(series):
    counts = series.value_counts()  # Calculate counts of unique values
    proportions = counts / counts.sum()  # Calculate proportions
    shannon_index = -np.sum(proportions * np.log(proportions))  # Shannon-Wiener formula
    return shannon_index

# Group by 'City' and apply the Shannon-Wiener index to 'Family', 'Genus', and 'Species' columns
shannon_family = df.groupby('City')['Family'].apply(shannon_wiener_index)
shannon_genus = df.groupby('City')['Genus'].apply(shannon_wiener_index)
shannon_species = df.groupby('City')['Species'].apply(shannon_wiener_index)

# Combine the results into a single DataFrame for comparison
shannon_indices_city = pd.DataFrame({
    'Shannon_Family': shannon_family,
    'Shannon_Genus': shannon_genus,
    'Shannon_Species': shannon_species
})

# Display the result
print(shannon_indices_city)

## Calculate Shannon Wiener Index for each Dissemination Area
# Group by 'DAUID' and apply the Shannon-Wiener index to 'Family', 'Genus', and 'Species' columns
shannon_family_dauid = df.groupby('DAUID')['Family'].apply(shannon_wiener_index)
shannon_genus_dauid = df.groupby('DAUID')['Genus'].apply(shannon_wiener_index)
shannon_species_dauid = df.groupby('DAUID')['Species'].apply(shannon_wiener_index)

# Combine the results into a single DataFrame for comparison
shannon_indices_dauid = pd.DataFrame({
    'Shannon_Family': shannon_family_dauid,
    'Shannon_Genus': shannon_genus_dauid,
    'Shannon_Species': shannon_species_dauid
})

shannon_indices_dauid = shannon_indices_dauid.merge(master_df, how='left', on='DAUID')

# Display the result
print(shannon_indices_dauid)

## Assign Downtown Label to Downtown
downtown_df = shannon_indices_dauid.merge(downtown_index, how='left', on='DAUID')
included_cities = ['Moncton', 'Fredericton', 'Quebec City', 'Longueuil', 'Montreal', 'Ottawa', 'Kingston',
 'Toronto', 'St. Catherines', 'Kitchener', 'Guelph', 'Windsor', 'Winnipeg', 'Regina', 'Lethbridge', 'Calgary',
 'Edmonton', 'Kelowna', 'Vancouver', 'Victoria', 'Mississauga', 'Burlington', 'Waterloo']
downtown_df = downtown_df[downtown_df['CITY'].isin(included_cities)]

downtown_df['DOWNTOWN'] = np.where(downtown_df['DOWNTOWN'] == 'Downtown', 1, 0)
cities = downtown_df['CITY'].unique()

print(downtown_df)
downtown_df.to_csv(r'C:\Users\alexj\Documents\Research\Canadian Urban Forest Inventories - Structure and Diversity\Python Scripts and Datasets\(4) Downtown Diversity.csv', index=False)


# Function to perform Mann-Whitney U test for each city and diversity index
def mann_whitney_test(city_df, column):
    downtown_group = city_df[city_df['DOWNTOWN'] == 1][column]
    non_downtown_group = city_df[city_df['DOWNTOWN'] == 0][column]

    # Perform Mann-Whitney U test only if both groups have data
    if len(downtown_group) > 0 and len(non_downtown_group) > 0:
        stat, p_value = mannwhitneyu(downtown_group, non_downtown_group, alternative='two-sided')
        return pd.Series({'Mann-Whitney U Statistic': stat, 'P-value': p_value})
    else:
        return pd.Series({'Mann-Whitney U Statistic': np.nan, 'P-value': np.nan})


# Apply Mann-Whitney U test for each city and each diversity index
def apply_tests(df):
    results = []
    indices = ['Shannon_Family', 'Shannon_Genus', 'Shannon_Species']

    for index in indices:
        # Select only the columns needed after applying the groupby
        result = df.groupby('CITY').apply(mann_whitney_test, column=index).reset_index(drop=True)
        result['CITY'] = df['CITY']  # Add the City column back explicitly
        result['Diversity_Index'] = index
        results.append(result)

    # Combine results for all indices into a single DataFrame
    combined_results = pd.concat(results, ignore_index=True)
    return combined_results

# Apply Mann-Whitney U test for each city
mann_whitney_results = apply_tests(downtown_df)

# Display the results
print(mann_whitney_results)
