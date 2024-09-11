# This code is based on the work of Morgenroth et al. (2020) (DOI: 10.3390/f11020135)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from scipy.stats import skew
import matplotlib.lines as mlines

df = pd.read_csv("data/wd/cleaned_master.csv", low_memory=False)
excluded_cities = ['Maple Ridge', 'New Westminster', 'Peterborough', 'Halifax']
df = df[~df['City'].isin(excluded_cities)]

# Data for Region Name
data_region = {
    "City": ['Victoria', 'Vancouver', 'New Westminster', 'Maple Ridge', 'Kelowna', 'Calgary', 'Edmonton',
             'Strathcona County', 'Lethbridge', 'Regina', 'Winnipeg', 'Windsor', 'Waterloo', 'Kitchener', 'Guelph',
             'Burlington', 'Mississauga', 'Toronto', 'Welland', 'St. Catharines', 'Niagara Falls', 'Ajax', 'Whitby',
             'Peterborough', 'Kingston', 'Ottawa', 'Montreal', 'Longueuil', 'Quebec City', 'Fredericton', 'Moncton',
             'Halifax'],
    "Ecozone": ['BC', 'BC', 'BC', 'BC', 'BC', 'Prairie', 'Prairie', 'Prairie', 'Prairie', 'Prairie', 'Prairie',
                'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario',
                'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec',
                'Atlantic', 'Atlantic', 'Atlantic']
}
region_df = pd.DataFrame(data_region)

city_to_region = dict(zip(region_df['City'], region_df['Region']))
df['Region'] = df['City'].map(city_to_region)
print(df.head())

# Data for Ecozone Name
data_ecozone = {
    "City": ['Victoria', 'Vancouver', 'New Westminster', 'Maple Ridge', 'Kelowna', 'Calgary', 'Edmonton',
             'Strathcona County', 'Lethbridge', 'Regina', 'Winnipeg', 'Windsor', 'Waterloo', 'Kitchener', 'Guelph',
             'Burlington', 'Mississauga', 'Toronto', 'Welland', 'St. Catharines', 'Niagara Falls', 'Ajax', 'Whitby',
             'Peterborough', 'Kingston', 'Ottawa', 'Montreal', 'Longueuil', 'Quebec City', 'Fredericton', 'Moncton',
             'Halifax'],
    "Ecozone": ['Pacific Maritime', 'Pacific Maritime', 'Pacific Maritime', 'Pacific Maritime', 'Montane Cordillera',
                  'Prairie', 'Prairie', 'Prairie', 'Prairie', 'Prairie', 'Prairie', 'Mixedwood Plain', 'Mixedwood Plain',
                  'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain',
                  'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain',
                  'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain', 'Mixedwood Plain',
                  'Mixedwood Plain', 'Atlantic Maritime', 'Atlantic Maritime', 'Atlantic Maritime']
}
ecozone_df = pd.DataFrame(data_ecozone)

city_to_ecozone = dict(zip(ecozone_df['City'], ecozone_df['Ecozone']))
df['Ecozone'] = df['City'].map(city_to_ecozone)
print(df.head())

# Ensure DBH is numeric and drop NaN values
df['DBH'] = pd.to_numeric(df['DBH'], errors='coerce')
df = df.dropna(subset=['DBH'])

# Create bins
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, np.inf]
n_classes = 17 # Number of DBH classes for each city
bin_midpoints = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins)-1)]

# Define cities and prepare lists for all midpoints and proportions
cities = df['City'].unique()
ecozones = df['Ecozone'].unique()
regions = df['Region'].unique()
all_midpoints = []
all_proportions = []

## Find Median DBH
# For each city
median_dbh_per_city = df.groupby('City')['DBH'].median().reset_index()
print(median_dbh_per_city)
city_skewness = df.groupby('City')['DBH'].apply(lambda x: skew(x, nan_policy='omit')).reset_index()
print(city_skewness)

# For each region
median_dbh_per_region = df.groupby('Region')['DBH'].median().reset_index()
print(median_dbh_per_region)
region_skewness = df.groupby('Region')['DBH'].apply(lambda x: skew(x, nan_policy='omit')).reset_index()
print(region_skewness)

# For each ecozone
median_dbh_per_ecozone = df.groupby('Ecozone')['DBH'].median().reset_index()
print(median_dbh_per_ecozone)
ecozone_skewness = df.groupby('Ecozone')['DBH'].apply(lambda x: skew(x, nan_policy='omit')).reset_index()
print(ecozone_skewness)

## Create histograms for the DBH distributions of each city (Urban Forest Diameter Class Distributions)
# Loop over each city to create histograms and curve plots
for city in cities:
    city_data = df[df['City'] == city]

    if len(city_data) == 0:
        continue  # Skip if there are no valid DBH values for the city

    # Create histogram with custom bins
    plt.figure(figsize=(8, 6))

    # Restrict x-axis to maximum of 150 cm
    sns.histplot(city_data['DBH'], bins=bins, kde=False, color='skyblue')

    # Fit and plot the KDE (Kernel Density Estimate) curve
    kde = gaussian_kde(city_data['DBH'])

    # Restrict the x-range for the KDE to be within the defined bin range
    x_range = np.linspace(0, 150, 1000)  # Limit the KDE to 150 cm
    plt.plot(x_range, kde(x_range) * len(city_data['DBH']) * (bins[1] - bins[0]), color='red', lw=2)

    # Set x-axis limit to match the bins
    plt.xlim(0, 150)

    # Add titles and labels
    plt.title(f'DBH Histogram with Curve for {city}')
    plt.xlabel('DBH (cm)')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()

## Create histograms for the DBH distributions of each region (Urban Forest Diameter Class Distributions)
# Loop over each city to create histograms and curve plots
for region in regions:
    region_data = df[df['Region'] == region]

    if len(region_data) == 0:
        continue  # Skip if there are no valid DBH values for the city

    # Create histogram with custom bins
    plt.figure(figsize=(8, 6))

    # Restrict x-axis to maximum of 150 cm
    sns.histplot(region_data['DBH'], bins=bins, kde=False, color='skyblue')

    # Fit and plot the KDE (Kernel Density Estimate) curve
    kde = gaussian_kde(region_data['DBH'])

    # Restrict the x-range for the KDE to be within the defined bin range
    x_range = np.linspace(0, 150, 1000)  # Limit the KDE to 150 cm
    plt.plot(x_range, kde(x_range) * len(region_data['DBH']) * (bins[1] - bins[0]), color='red', lw=2)

    # Set x-axis limit to match the bins
    plt.xlim(0, 150)

    # Add titles and labels
    plt.title(f'DBH Histogram with Curve for {region}')
    plt.xlabel('DBH (cm)')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()

## Create histograms for the DBH distributions of each ecozone (Urban Forest Diameter Class Distributions)
# Loop over each city to create histograms and curve plots
for ecozone in ecozones:
    ecozone_data = df[df['Ecozone'] == ecozone]

    if len(ecozone_data) == 0:
        continue  # Skip if there are no valid DBH values for the city

    # Create histogram with custom bins
    plt.figure(figsize=(8, 6))

    # Restrict x-axis to maximum of 150 cm
    sns.histplot(ecozone_data['DBH'], bins=bins, kde=False, color='skyblue')

    # Fit and plot the KDE (Kernel Density Estimate) curve
    kde = gaussian_kde(ecozone_data['DBH'])

    # Restrict the x-range for the KDE to be within the defined bin range
    x_range = np.linspace(0, 150, 1000)  # Limit the KDE to 150 cm
    plt.plot(x_range, kde(x_range) * len(ecozone_data['DBH']) * (bins[1] - bins[0]), color='red', lw=2)

    # Set x-axis limit to match the bins
    plt.xlim(0, 150)

    # Add titles and labels
    plt.title(f'DBH Histogram with Curve for {ecozone}')
    plt.xlabel('DBH (cm)')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()

## Comparison of Diameter Class Distributions Against Richards Distribution
plt.figure(figsize=(12, 6)) #

# Richards data points and line function
richards_midpoints = [10, 30, 50, 70]
richards_values = [40, 30, 20, 10]
x = np.linspace(0, 100, 6)
y = -0.5 * x + 45

# Plot Richards data and line
plt.plot(richards_midpoints, richards_values, 'bs-', label='Richards Data')
plt.plot(x, y, 'b-', label='Line: y = -0.5x + 45')

# Loop through each city and calculate DBH proportions
for city in cities:
    city_data = df[df['City'] == city]

    # Bin the DBH values and calculate the proportion in each bin
    city_data['DBH_bins'] = pd.cut(city_data['DBH'], bins=bins)
    bin_counts = city_data['DBH_bins'].value_counts().sort_index()

    # Calculate the proportion of the total population in each bin
    proportions = bin_counts / bin_counts.sum() * 100  # Convert to percentages

    # Plot the proportions for this city (only markers, no lines)
    plt.plot(bin_midpoints, proportions, 'o', markersize=4, markerfacecolor='k', markeredgewidth=0, label=f'{city} Data')

# Create a line of best fit
x_fit = np.linspace(0, 150, 1000)
y_fit = 41.543 * np.exp(-0.039 * x_fit)
plt.plot(x_fit, y_fit, 'k-', label='Line of Best Fit')

# Legend
inventory_data_handle = mlines.Line2D([], [], color='k', marker='o', linestyle='None', markersize=8, label='Inventory Data')
best_fit_handle = mlines.Line2D([], [], color='k', linestyle='-', markersize=8, label='Line of Best Fit')
richards_handle = mlines.Line2D([], [], color='b', marker='s', linestyle='-', markersize=8, label='Richards')
plt.legend(handles=[inventory_data_handle, best_fit_handle, richards_handle])

# Customize plot
plt.xlim(0, 150)
plt.ylim(0, 70)
plt.title('Aggregated DBH Distribution and Line of Best Fit')
plt.xlabel('DBH (cm)')
plt.ylabel('Proportion of Total Population (%)')
plt.grid(False)
plt.show()


## Structural Diversity Index
# Calculate Shannon-Wiener index for each city
def calculate_shannon_wiener_city(city_data, bins):
    # Classify trees into DBH classes using binning
    dbh_classes = pd.cut(city_data['DBH'], bins=bins, labels=range(1, len(bins)))

    # Calculate the proportion of trees in each class
    class_counts = dbh_classes.value_counts(normalize=True).sort_index()

    # Check for empty upper bins and adjust the number of classes
    last_non_empty_class = class_counts[class_counts > 0].index[-1]
    valid_bins = bins[:last_non_empty_class + 1]  # Include up to the last non-empty class

    # Reclassify using valid bins
    dbh_classes = pd.cut(city_data['DBH'], bins=valid_bins, labels=range(1, len(valid_bins)))
    class_counts = dbh_classes.value_counts(normalize=True).sort_index()

    # Filter out zero proportions to avoid log(0)
    class_proportions = class_counts[class_counts > 0]

    # Calculate the Shannon-Wiener index (H)
    H = -np.sum(class_proportions * np.log(class_proportions))

    # Calculate H_max (maximum possible diversity)
    H_max = np.log(len(valid_bins) - 1)  # Use the number of non-empty bins

    return H, H_max

city_results = []

cities = df['City'].unique()
for city in cities:
    city_data = df[df['City'] == city]

    if len(city_data) == 0:
        continue  # Skip if there are no valid DBH values for the city

    H, H_max = calculate_shannon_wiener_city(city_data, bins)

    # Store the result for the city
    city_results.append({
        'City': city,
        'Shannon-Wiener Index (H)': H,
        'Maximum Diversity (H_max)': H_max
    })

# Calculate Shannon-Wiener index for each region
def calculate_shannon_wiener_region(region_data, bins):
    # Classify trees into DBH classes using binning
    dbh_classes = pd.cut(region_data['DBH'], bins=bins, labels=range(1, len(bins)))

    # Calculate the proportion of trees in each class
    class_counts = dbh_classes.value_counts(normalize=True).sort_index()

    # Check for empty upper bins and adjust the number of classes
    last_non_empty_class = class_counts[class_counts > 0].index[-1]
    valid_bins = bins[:last_non_empty_class + 1]  # Include up to the last non-empty class

    # Reclassify using valid bins
    dbh_classes = pd.cut(region_data['DBH'], bins=valid_bins, labels=range(1, len(valid_bins)))
    class_counts = dbh_classes.value_counts(normalize=True).sort_index()

    # Filter out zero proportions to avoid log(0)
    class_proportions = class_counts[class_counts > 0]

    # Calculate the Shannon-Wiener index (H)
    H = -np.sum(class_proportions * np.log(class_proportions))

    # Calculate H_max (maximum possible diversity)
    H_max = np.log(len(valid_bins) - 1)  # Use the number of non-empty bins

    return H, H_max

region_results = []

regions = df['Region'].unique()
for region in regions:
    region_data = df[df['Region'] == region]

    if len(region_data) == 0:
        continue  # Skip if there are no valid DBH values for the city

    H, H_max = calculate_shannon_wiener_region(region_data, bins)

    # Store the result for the city
    region_results.append({
        'Region': region,
        'Shannon-Wiener Index (H)': H,
        'Maximum Diversity (H_max)': H_max
    })

# Calculate Shannon-Wiener index for each ecozone
def calculate_shannon_wiener_ecozone(ecozone_data, bins):
    # Classify trees into DBH classes using binning
    dbh_classes = pd.cut(ecozone_data['DBH'], bins=bins, labels=range(1, len(bins)))

    # Calculate the proportion of trees in each class
    class_counts = dbh_classes.value_counts(normalize=True).sort_index()

    # Check for empty upper bins and adjust the number of classes
    last_non_empty_class = class_counts[class_counts > 0].index[-1]
    valid_bins = bins[:last_non_empty_class + 1]  # Include up to the last non-empty class

    # Reclassify using valid bins
    dbh_classes = pd.cut(ecozone_data['DBH'], bins=valid_bins, labels=range(1, len(valid_bins)))
    class_counts = dbh_classes.value_counts(normalize=True).sort_index()

    # Filter out zero proportions to avoid log(0)
    class_proportions = class_counts[class_counts > 0]

    # Calculate the Shannon-Wiener index (H)
    H = -np.sum(class_proportions * np.log(class_proportions))

    # Calculate H_max (maximum possible diversity)
    H_max = np.log(len(valid_bins) - 1)  # Use the number of non-empty bins

    return H, H_max

ecozone_results = []

ecozones = df['Ecozone'].unique()
for ecozone in ecozones:
    ecozone_data = df[df['Ecozone'] == ecozone]

    if len(ecozone_data) == 0:
        continue  # Skip if there are no valid DBH values for the city

    H, H_max = calculate_shannon_wiener_city(ecozone_data, bins)

    # Store the result for the city
    ecozone_results.append({
        'Ecozone': ecozone,
        'Shannon-Wiener Index (H)': H,
        'Maximum Diversity (H_max)': H_max
    })

# Convert results to a DataFrame for easy viewing
Structural_Diversity_Index_city_df = pd.DataFrame(city_results)
print(Structural_Diversity_Index_city_df)
Structural_Diversity_Index_region_df = pd.DataFrame(region_results)
print(Structural_Diversity_Index_region_df)
Structural_Diversity_Index_ecozone_df = pd.DataFrame(ecozone_results)
print(Structural_Diversity_Index_ecozone_df)
