# This code is based on the work of Ma et al. (2020) (DOI: 10.1016/j.ufug.2020.126826)

import pandas as pd
import numpy as np

df = pd.read_csv("data/wd/cleaned_master.csv", low_memory=False)

# Print the list of headers
headers = df.columns.tolist()
print("List of headers in cleaned_master.csv:")
print(headers)

# Identify Species
def extract_species(row):
    if isinstance(row['Botanical Name'], str):
        if row['City'] in ['Moncton']:
            return row['Botanical Name'][:6]
        if row['City'] in ['Mississauga']:
            return row['Botanical Name'][:4]
        if row['City'] in ['Halifax']:
            return row['Botanical Name'][:4]
        else:
            words = row['Botanical Name'].split()
            if len(words) > 1:
                return ' '.join(words[:2])  # Join the first two words
            elif len(words) == 1:
                return words[0]  # If there's only one word, return it
    return np.nan  # Handle cases where 'Botanical Name' is not a string or is empty

# Print the list of species
df['Species'] = df.apply(extract_species, axis=1) # Applies the function to each row and creates a Species column
species_list = df['Species'].dropna().unique().tolist() # Drop any NaN values in the species column
print("List of Species:")
for species in species_list:
    print(species)

# Quantify the number of species
unique_species_count = len(species_list)
print(f"\nTotal number of unique species: {unique_species_count}")

# Identify Genus
def extract_genus(row):
    if isinstance(row['Botanical Name'], str):
        if row['City'] in ['Moncton']:
            return row['Botanical Name'][:3]
        if row['City'] in ['Mississauga']:
            return row['Botanical Name'][:2]
        if row['City'] in ['Halifax']:
            return row['Botanical Name'][:2]
        elif len(row['Botanical Name'].split()) > 0:
            return row['Botanical Name'].split()[0]
    return np.nan

# Print the list of gemera
df['Genus'] = df.apply(extract_genus, axis=1) # Applies the function to each row and creates a Genus column
genus_list = df['Genus'].dropna().unique().tolist() # Drop any NaN values in the species column
print("List of Genera:")
for genus in genus_list:
    print(genus)

# Quantify the number of genera
unique_genus_count = len(genus_list)
print(f"\nTotal number of unique genera: {unique_genus_count}")


### @ Lukas - notes to add
# Determine top six species for each City
# Calculate what proportion of the street tree inventory for a given City is made up of their most common (top) six species
# Calculate shannon index and inverse simpson index for species, genus, and family
# Determine families for each genera


