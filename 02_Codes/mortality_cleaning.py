# %%
# Import libraries
import pandas as pd
import numpy as np
import glob

# Load one dataset to check constaints
m2007 = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2006.txt?token=GHSAT0AAAAAACWW3VV4VLIGBYI42XW65YPEZ2D6A2Q",
    sep="\t",  # Tab as delimiter
)
m2007

# %%
urls = [
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2003.txt?token=GHSAT0AAAAAACWW3VV5P6VL3TCMD4H4OP3KZ2D6HEQ",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2004.txt?token=GHSAT0AAAAAACWW3VV4NXP226CFJMU5N23SZ2D6HXQ",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2005.txt?token=GHSAT0AAAAAACWW3VV52R6QJSFC7AY3Y5XYZ2D6IIA",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2006.txt?token=GHSAT0AAAAAACWW3VV4VLIGBYI42XW65YPEZ2D6A2Q",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2007.txt?token=GHSAT0AAAAAACWW3VV52NAXZ5MT7MGRL3L6Z2D6BWQ",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2008.txt?token=GHSAT0AAAAAACWW3VV4UCC4SDNEXCO3EDGIZ2D6CSQ",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2009.txt?token=GHSAT0AAAAAACWW3VV44BHW7WYBDFUFNPSSZ2D6C7Q",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2010.txt?token=GHSAT0AAAAAACWW3VV4A2GVVXEGJNXXFUOSZ2D6DZQ",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2011.txt?token=GHSAT0AAAAAACWW3VV5TFS3XASF75DMFITUZ2D6ECA",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2012.txt?token=GHSAT0AAAAAACWW3VV54FXII7GK5LFXIAJGZ2D6EJQ",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2013.txt?token=GHSAT0AAAAAACWW3VV5NYWIACTT6A66OXREZ2D6ERA",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2014.txt?token=GHSAT0AAAAAACWW3VV4I3CG2GPPKUXXQ4BKZ2D6E4Q",
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/tursunait-mortality-1/01_Data/01_Raw/Mortality_US_VitalStatistics/2015.txt?token=GHSAT0AAAAAACWW3VV5XDPVYQ64PZRH7RWMZ2D6FEQ",
]

# Initialize a list to hold DataFrames
dataframes = []

for url in urls:
    try:
        # Read the file into a DataFrame
        df = pd.read_csv(url, sep="\t", engine="python", skipfooter=15)
        dataframes.append(df)
    except Exception as e:
        print(f"Error reading file {url}: {e}")

# Combine all DataFrames
merged_mortality = pd.concat(dataframes, ignore_index=True)

# Display a preview of the merged DataFrame
print("Merged DataFrame preview:")
merged_mortality

# %%
# Summary of the dataset
print(merged_mortality.info())

# Check for missing values
print(merged_mortality.isnull().sum())

# Get basic statistics
print(merged_mortality.describe())

# %%
print(merged_mortality["County"].nunique())

# %%
# Check datatpes
merged_mortality.dtypes

# %%
merged_mortality["Year Code"] = merged_mortality["Year Code"].astype(int)
merged_mortality["Year"] = merged_mortality["Year"].astype(int)
merged_mortality.dtypes

# %%
# Display unique values in the 'Year Code' column
unique_year_codes = merged_mortality["Year Code"].unique()
unique_year_codes.sort()
print("Unique values in 'Year Code':")
print(unique_year_codes)

# %%
# Splitting 'County' column into 'County' and 'State'
merged_mortality[["County", "State"]] = merged_mortality["County"].str.rsplit(
    ", ", n=1, expand=True
)

# Check the first few rows to verify
merged_mortality

# %%
# Drop 'Year Code' and 'Notes' columns
merged_mortality.drop(columns=["Year Code", "Notes"], inplace=True)

# Verify the columns are removed
merged_mortality

# %%
# Specify the desired column order
desired_order = [
    "State",
    "County",
    "County Code",
    "Year",
    "Drug/Alcohol Induced Cause",
    "Drug/Alcohol Induced Cause Code",
    "Deaths",
]
# Reorder columns
merged_mortality = merged_mortality[desired_order]
# Verify the new column order
merged_mortality

# %%
print(merged_mortality["Drug/Alcohol Induced Cause Code"].unique())
print(merged_mortality["Drug/Alcohol Induced Cause"].unique())

# %%
# Drop rows where Drug/Alcohol Induced Cause is 'All other non-drug and non-alcohol causes'
merged_mortality = merged_mortality[
    merged_mortality["Drug/Alcohol Induced Cause Code"] != "O9"
]
# Drop rows where Drug/Alcohol Induced Cause is 'All other alcohol-induced causes'
merged_mortality = merged_mortality[
    merged_mortality["Drug/Alcohol Induced Cause Code"] != "A9"
]
# Drop rows where Drug/Alcohol Induced Cause is 'Alcohol poisonings (overdose) (X45, X65, Y15)'
merged_mortality = merged_mortality[
    merged_mortality["Drug/Alcohol Induced Cause Code"] != "A1"
]
# Drop rows where Drug/Alcohol Induced Cause is 'All other drug-induced causes'
merged_mortality = merged_mortality[
    merged_mortality["Drug/Alcohol Induced Cause Code"] != "D9"
]
# Verify the result
print(merged_mortality["Drug/Alcohol Induced Cause Code"].unique())

# %%
merged_mortality

# %%
print(merged_mortality["Drug/Alcohol Induced Cause Code"].unique())
print(merged_mortality["Drug/Alcohol Induced Cause"].unique())

# %%
merged_mortality["State"].unique()

# %%
all_unique_deaths = merged_mortality["Deaths"].unique().tolist()
print(all_unique_deaths)

# %%
merged_mortality

# %%
merged_mortality[merged_mortality["Deaths"] == "Missing"]

# %%
merged_mortality["Deaths"] = pd.to_numeric(merged_mortality["Deaths"], errors="coerce")
# Check for non-numeric values and missing entries
print("Unique values after conversion:")
print(merged_mortality["Deaths"].unique())

# Count missing values
missing_deaths_count = merged_mortality["Deaths"].isnull().sum()
print(f"Number of missing or invalid death entries: {missing_deaths_count}")
merged_mortality[merged_mortality["Deaths"].isnull()]

# %%
# Drop columns for Drug/Alcohol Induced Cause Drug/Alcohol Induced Cause Code
merged_mortality.drop(
    columns=["Drug/Alcohol Induced Cause", "Drug/Alcohol Induced Cause Code"],
    inplace=True,
)
merged_mortality
merged_mortality.to_csv("all_states_mortality.csv", index=False)

print("Data saved to 'all_merged_mortality.csv'")

# %%
# Check if the
merged_mortality[merged_mortality["Deaths"].isnull()]

# %%
merged_mortality["State"] = merged_mortality["State"].astype(str)

# %%
merged_mortality = merged_mortality[
    merged_mortality["State"].isin(["FL", "WA", "GA", "NC", "SC", "CO", "OR", "MT"])
]
merged_mortality

# %%
merged_mortality = (
    merged_mortality.groupby(["State", "County", "County Code", "Year"])
    .sum()
    .reset_index()
)
merged_mortality

# %%
merged_mortality["Deaths"] = merged_mortality["Deaths"].astype(int)
merged_mortality["County"] = merged_mortality["County"].str.upper()
# Rename a column
merged_mortality.rename(columns={"County Code": "County_Code"}, inplace=True)
# Convert all column names to uppercase
merged_mortality.columns = merged_mortality.columns.str.upper()
merged_mortality["COUNTY"].nunique()

# %%
merged_mortality.to_csv("controls_merged_mortality.csv", index=False)

print("Data saved to 'controls_merged_mortality.csv'")

# %%
population_data = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/refs/heads/main/01_Data/03_Results/POPULATION_TRANSPOSE_1122.csv?token=GHSAT0AAAAAACWW3VV5BPNRAJE7QJCYG5UGZ2D4OPQ"
)
# Rename a column
population_data.rename(columns={"COUNTY CODE": "COUNTY_CODE"}, inplace=True)
population_data

# %%
# Summary of the dataset
print(population_data.info())

# Check for missing values
print(population_data.isnull().sum())

# Get basic statistics
print(population_data.describe())

# %%
population_data = population_data[
    population_data["YEAR"].isin(
        [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
    )
]
population_data["COUNTY_CODE"].nunique()

# %%
population_data = population_data[
    population_data["STATE"].isin(["FL", "WA", "GA", "NC", "SC", "CO", "OR", "MT"])
]
population_data["COUNTY_CODE"].nunique()

# %%
population_data.dtypes

# %%
combined_data = pd.merge(
    population_data,  # Population DataFrame
    merged_mortality,  # Mortality DataFrame
    on=["COUNTY_CODE", "YEAR"],  # Common columns for merging
    how="right",  # Outer join to capture all rows
    indicator=True,  # Add an indicator column to see match status
    suffixes=("_pop", "_mort"),  # Suffixes to differentiate COUNTY columns
)

# Display merged data with the indicator column
combined_data

# %%
# Identify mismatched COUNTY names
mismatched_counties = combined_data[
    combined_data["COUNTY_pop"].str.lower() != combined_data["COUNTY_mort"].str.lower()
]

print("Mismatched counties:")
print(
    mismatched_counties[
        ["COUNTY_CODE", "COUNTY_pop", "COUNTY_mort", "STATE_pop", "STATE_mort"]
    ]
)

# %%
# Summary of the merge result
print(combined_data["_merge"].value_counts())

# %%
combined_data[combined_data._merge != "both"]

# %%
combined_data
combined_data.drop(
    columns=["STATE_mort", "COUNTY_mort", "_merge"],
    inplace=True,
)
combined_data.rename(
    columns={"COUNTY_pop": "COUNTY", "STATE_pop": "STATE"}, inplace=True
)
combined_data

# %%
# Convert combined_data to a DataFrame
combined_data = pd.DataFrame(combined_data)

# Reorder columns
desired_order = [
    "STATE_NAME",
    "STATE",
    "COUNTY",
    "COUNTY_CODE",
    "YEAR",
    "POPULATION",
    "DEATHS",
]
combined_data = combined_data[desired_order]

combined_data

# %%
combined_data["DEATHS"].isnull().sum()

# %%
combined_data.to_csv("mortality_population.csv", index=False)

# %%
combined_data

# %%
# Group by STATE_NAME, STATE, and YEAR, and list unique counties
counties_per_state_year = (
    combined_data.groupby(["STATE_NAME", "STATE", "YEAR"])["COUNTY"]
    .unique()
    .reset_index(name="Counties_List")
)

# Display the result
counties_per_state_year
