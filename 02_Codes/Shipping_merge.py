# %% [markdown]
# # Opioid Shipment data merging
#

# %%
import pandas as pd

opd_df = pd.read_csv(
    "https://raw.githubusercontent.com/ISL-0111/personal_ISL/refs/heads/main/concatenated_shipping_data.csv?token=GHSAT0AAAAAAC2RLIBHNQMFOU2JPLK2W6PUZ2CZUZQ"
)
pop_0715_reshaped = pd.read_csv(
    "https://raw.githubusercontent.com/ISL-0111/personal_ISL/refs/heads/main/pop_0715_reshaped.csv?token=GHSAT0AAAAAAC2RLIBGNMP22UP2IRBWQ432Z2CZUDA"
)
fips_cleaned = pd.read_csv(
    "https://raw.githubusercontent.com/ISL-0111/personal_ISL/refs/heads/main/fips_data_cleaned.csv?token=GHSAT0AAAAAAC2RLIBG3MDWU4F6WJONOCAAZ2CZUNA"
)

# %% [markdown]
# #### Opioid Shipment + FIPS(County Code)

# %%
display(opd_df.sample(20))
display(opd_df.shape)

# Rename columns,
opd_df.columns = (
    opd_df.columns.str.replace("year", "YEAR")
    .str.replace("BUYER_STATE", "STATE")
    .str.replace("BUYER_COUNTY", "COUNTY")
    .str.replace("strength", "MME_Conversion_Factor")
)

opd_df["COUNTY"] = opd_df["COUNTY"] + " COUNTY"
display(opd_df.sample(10))
display(opd_df.dtypes)


# %%
### VOID : this code is to check if the opd_df contains state level data. ###
# sample1 = opd_df[(opd_df['COUNTY'] == 'NORTH CAROLINA') & (opd_df['STATE'] == 'NC')]
# sample2 = opd_df[(opd_df['COUNTY'] == 'NEW YORK') & (opd_df['STATE'] == 'NY')] ## Intrestingly there is a county named 'NEW YORK' in NY, and it was turned out NEW YORK county in NY.
# display(sample1)
# display(sample2)

# # To exclude state level data, clean index data first
# state_abb = state_abb.rename(columns={'Abbreviation' : 'STATE', 'State' : 'COUNTY'}) # temprarly rename the columns to clean data
# state_abb['COUNTY'] = state_abb['COUNTY'].str.upper()
# state_abb.head(5)

# drop the 'state' data in the opd_df
# filtered_opd_df = opd_df.merge(state_abb, on=['COUNTY', 'STATE'], how='left', indicator=True)
# filtered_opd_df = filtered_opd_df[filtered_opd_df['_merge'] == 'left_only'].drop(columns=['_merge'])

# display(filtered_opd_df.shape)

# %%
# Filter dataset for years 2007-2015 and select relevant states
subset_opd_df = opd_df[
    (opd_df["YEAR"] >= 2007)
    & (opd_df["YEAR"] <= 2015)
    & (opd_df["STATE"].isin(["FL", "GA", "NC", "SC", "WA", "CO", "OR", "MT"]))
][["STATE", "COUNTY", "YEAR", "MME_Conversion_Factor"]]

# Display 20 random rows from the subset
display(subset_opd_df.sample(20))

# Display the shape of the subset dataframe
display(subset_opd_df.shape)
# ROW 4952

# %%
# FIPS data set
fips_cleaned.rename(columns={"COUNTY": "COUNTY_CODE"}, inplace=True)
fips_cleaned.rename(columns={"COUNTY_NAME": "COUNTY"}, inplace=True)
fips_cleaned.head(5)

# %%
subset_opd_merged = subset_opd_df.merge(
    fips_cleaned[["STATE", "COUNTY", "COUNTY_CODE"]],  # Select only necessary columns
    on=["STATE", "COUNTY"],  # Columns to join on
    how="left",  # Use 'left' to keep all rows from subset_opd_clean
    indicator=True,
)
subset_opd_merged.columns
display(subset_opd_merged["_merge"].value_counts())

left_only_rows = subset_opd_merged[subset_opd_merged["_merge"] == "left_only"]
display(left_only_rows)

# %%
subset_opd_clean = subset_opd_merged.copy()
# Cleaning data set
# [1] BURLINGTON COUNTY, MT may not exist in real. Therefore I drop those rows.
subset_opd_clean = subset_opd_clean[subset_opd_clean["COUNTY"] != "BURLINGTON COUNTY"]
# [2] Change name in 'SAINT' to 'ST.' in the county column to match
subset_opd_clean["COUNTY"] = subset_opd_clean["COUNTY"].str.replace("SAINT", "ST.")
# [3] DE SOTO COUNTUY -> DESOTO COUNTY
subset_opd_clean["COUNTY"] = subset_opd_clean["COUNTY"].str.replace("DE SOTO", "DESOTO")

# %%
subset_opd_clean = subset_opd_clean.drop(columns=["_merge"])

# Perform the merge again
subset_opd_merged_fips = pd.merge(
    subset_opd_clean,
    fips_cleaned[["STATE", "COUNTY", "COUNTY_CODE"]],
    on=["STATE", "COUNTY"],
    how="left",
    indicator=True,
)
display(subset_opd_merged_fips["_merge"].value_counts())
subset_opd_merged_fips = subset_opd_merged_fips.drop(columns=["_merge"])
subset_opd_merged_fips = subset_opd_merged_fips.drop(columns=["COUNTY_CODE_x"])
subset_opd_merged_fips = subset_opd_merged_fips.rename(
    columns={"COUNTY_CODE_y": "COUNTY_CODE"}
)
display(subset_opd_merged_fips.sample(10))

# %% [markdown]
# #### Opiod shipment + FIPS(County Code) + 'Populatinon'

# %%
# Population date
display(pop_0715_reshaped.head(10))
display(pop_0715_reshaped.shape)

# %% [markdown]
# Merging population data into opioid shipment data

# %%
# Subset the population data for the relevant states
subset_pop_0715 = pop_0715_reshaped[
    pop_0715_reshaped["STATE"].isin(["FL", "GA", "NC", "SC", "WA", "CO", "OR", "MT"])
]
subset_pop_0715_clean = subset_pop_0715.copy()
display(subset_pop_0715_clean["STATE"].unique())
display(subset_pop_0715_clean.sample(10))
display(subset_pop_0715_clean.shape)

# %%
merged_shipping = pd.merge(
    subset_pop_0715_clean,
    subset_opd_merged_fips,
    on=["STATE", "COUNTY", "COUNTY_CODE", "YEAR"],
    how="left",
    indicator=True,
)
display(merged_shipping.sample(10))
display(merged_shipping["_merge"].value_counts())
left_value = merged_shipping[merged_shipping["_merge"] == "left_only"]

display(left_value)  # MME is '0' is left only rows

# %%
# Fill the missing values in the MME_Conversion_Factor column with 0 & drop _merge column
merged_shipping = merged_shipping.drop(columns=["_merge"])
merged_shipping["MME_Conversion_Factor"] = merged_shipping[
    "MME_Conversion_Factor"
].fillna("0")
merged_shipping.head(5)


# %%
merged_shipping.dtypes
merged_shipping["MME_Conversion_Factor"] = merged_shipping[
    "MME_Conversion_Factor"
].astype(float)
merged_shipping["MME_per_capita"] = (
    merged_shipping["MME_Conversion_Factor"] / merged_shipping["POPULATION"]
)

merged_shipping.head(5)

# %%
merged_shipping.to_csv("shipping_merged_07_15.csv", index=False)
print("CSV file saved")

# %% [markdown]
# # Appendix
# List of conties MME_Conversaion_Facot is '0'

# %%
MME_0 = merged_shipping[merged_shipping["MME_Conversion_Factor"] == 0]
print(MME_0)
