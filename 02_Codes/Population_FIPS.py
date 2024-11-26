# %% [markdown]
# # Population dataset
#
# #### Source
# - 1. Population data (2000~2010), US  Census Bureau
# - 2. Population data (2010~2020), US  Census Bureau
# - 3. FIPS : https://raw.githubusercontent.com/wpinvestigative/arcos-api/refs/heads/master/data/county_fips.csv
#
# ### Remark
# - Target year : 2007 ~ 2015
# - FIPS(~2010 only) : Shannon County(SD) -> Oglala Lakota County(SD)
# - FIPS(2010~ only) : Bedford City(VA) -> Bedford County(VA)
#  * Alaska is excluded
#

# %%
import pandas as pd

pop_0010 = pd.read_csv(
    "/Users/ilseoplee/Desktop/Study/2024 MIDS/Practical Data Science/Final_Opioid_Project/00_soure_data/Population/Raw/co-est00int-agesex-5yr.csv",
    encoding="utf-8",
)
pop_1020 = pd.read_csv(
    "/Users/ilseoplee/Desktop/Study/2024 MIDS/Practical Data Science/Final_Opioid_Project/00_soure_data/Population/Raw/co-est2020.csv",
    encoding="utf-8",
)
fips = pd.read_csv(
    "/Users/ilseoplee/Desktop/Study/2024 MIDS/Practical Data Science/Final_Opioid_Project/00_soure_data/Population/fips_master.csv",
    encoding="utf-8",
)
state_abbreviation = pd.read_csv(
    "https://raw.githubusercontent.com/jasonong/List-of-US-States/refs/heads/master/states.csv",
    encoding="utf-8",
)

# %% [markdown]
# #### 1. Fips data cleaning
# - 'state column' 'NA' is all not about states (Unites states, Alabama, California, Idaho..)
# - duplication check and drop, data type check

# %%
display(fips.sample(10))
display(fips.dtypes)

# %%
# Duplication & Data type check
# fips.dtypes
# fips["duplicate"] = fips.duplicated() ## Duplication check
# fips["duplicate"].value_counts() ## There is no duplication
# fips = fips.drop(columns=['duplicate']) ## Drop the column
fips["state"].unique()

# %%
# The 'state' colunm with NaN in 'state' not 'county' Thus I will delete the rows with NA value
NaN_fips = fips[fips["state"].isna()]
print(NaN_fips)
len(NaN_fips)

# Drop the NaN
fips_drop_NaN = fips.dropna(subset=["state"])
fips_drop_NaN["state"].unique()

# %%
# Import state name data, format the state name and abbreviation to match the fips data
state_abbreviation["State"] = state_abbreviation["State"].str.upper()
state_abbreviation = state_abbreviation.rename(
    columns={"Abbreviation": "state", "State": "state_name"}
)
state_abbreviation.head(3)

# %%
# Merge the fips data with state name data
fips_state_abb = pd.merge(fips_drop_NaN, state_abbreviation, how="left", on="state")
fips_state_abb["state_name"].unique()  # No missing value
fips_state_abb = fips_state_abb.rename(
    columns={
        "fips": "COUNTY",
        "name": "COUNTY_NAME",
        "state": "STATE",
        "state_name": "STATE_NAME",
    }
)
fips_state_abb["COUNTY_NAME"] = fips_state_abb["COUNTY_NAME"].str.upper()
fips_cleaned = fips_state_abb
fips_cleaned.head(3)

# fips_cleaned.to_csv('fips_data_cleaned.csv', index=False)
# print("CSV file saved")

# %% [markdown]
# #### 2. Population data cleaning

# %%
# Missing value check
display(pop_0010.head(6))
display(print(pop_0010.dtypes))
pop_0010 = pop_0010.fillna(0)

# %%
# data type conversion
float_columns = pop_0010.select_dtypes(include=["float64"]).columns
pop_0010[float_columns] = pop_0010[float_columns].fillna(0).astype("int64")
display(print(pop_0010.dtypes))

# %%
#  Population 2000-2010 : drop the unncessary rows, change the column names for formatting
pop_0010_cleaned = pop_0010.copy()

pop_0010_cleaned = pop_0010_cleaned[
    (pop_0010_cleaned["SEX"] == 0) & (pop_0010_cleaned["AGEGRP"] == 0)
]  # both SEX & AGEGRP = 0 is target rows
pop_0010_cleaned = pop_0010_cleaned.drop(
    columns=[
        "ESTIMATESBASE2000",
        "SUMLEV",
        "STATE",
        "COUNTY",
        "SEX",
        "AGEGRP",
        "CENSUS2010POP",
        "POPESTIMATE2010",
    ]
)

pop_0010_cleaned["STNAME"] = pop_0010_cleaned["STNAME"].str.upper()
pop_0010_cleaned["CTYNAME"] = pop_0010_cleaned["CTYNAME"].str.upper()

pop_0010_cleaned.columns = (
    pop_0010_cleaned.columns.str.replace("POPESTIMATE", "")
    .str.replace("STNAME", "STATE_NAME")
    .str.replace("CTYNAME", "COUNTY")
)

pop_0010_cleaned["COUNTY"] = pop_0010_cleaned["COUNTY"].str.replace(
    "DOÒA ANA COUNTY", "DONA ANA COUNTY"
)  # from 3. Data Cleaning
pop_0010_cleaned = pop_0010_cleaned[
    (pop_0010_cleaned["STATE_NAME"] != pop_0010_cleaned["COUNTY"])
    | (pop_0010_cleaned["STATE_NAME"] == "DISTRICT OF COLUMBIA")
]  # # from 3. Data Cleaning

pop_0010_cleaned.head(3)

# %%
display(pop_1020.head(3))
display(pop_1020.dtypes)
pop_1020 = pop_1020.fillna(0)

# %%
# #  Population 2010-2020 : drop the unncessary rows, change the column names for formatting
pop_1020_cleaned = pop_1020.copy()

pop_1020_cleaned = pop_1020.drop(
    columns=[
        "CENSUS2010POP",
        "ESTIMATESBASE2010",
        "SUMLEV",
        "REGION",
        "DIVISION",
        "STATE",
        "POPESTIMATE042020",
        "COUNTY",
    ]
)

pop_1020_cleaned["STNAME"] = pop_1020_cleaned["STNAME"].str.upper()
pop_1020_cleaned["CTYNAME"] = pop_1020_cleaned["CTYNAME"].str.upper()

pop_1020_cleaned.columns = (
    pop_1020_cleaned.columns.str.replace("POPESTIMATE", "")
    .str.replace("STNAME", "STATE_NAME")
    .str.replace("CTYNAME", "COUNTY")
)

pop_1020_cleaned["COUNTY"] = pop_1020_cleaned["COUNTY"].str.replace(
    "DOÒA ANA COUNTY", "DONA ANA COUNTY"
)  # from 3. Data Cleaning
print((pop_1020_cleaned["COUNTY"] == "DONA ANA COUNTY").sum())
pop_1020_cleaned = pop_1020_cleaned[
    (pop_1020_cleaned["STATE_NAME"] != pop_1020_cleaned["COUNTY"])
    | (pop_1020_cleaned["STATE_NAME"] == "DISTRICT OF COLUMBIA")
]  # District of Clumbia is exception

pop_1020_cleaned.head(3)

# %% [markdown]
# 3. Merging table : Population 2000~2010 + Population 2010~2020

# %%
pop_0020_test = pd.merge(
    pop_0010_cleaned,
    pop_1020_cleaned,
    how="outer",
    on=["STATE_NAME", "COUNTY"],
    indicator=True,
)
pop_0020_test["_merge"].value_counts()

pop_0020_test_match = pop_0020_test[
    (pop_0020_test["_merge"] == "left_only") | (pop_0020_test["_merge"] == "right_only")
]  # | is 'OR'
print(pop_0020_test_match)

# %% [markdown]
# #### Remarks
#     - ALASKA is not included in this sutdy
#     - LOUISIANA LA SALLE PARISH => Indent error => fix the error
#     - SOUTH DAKOTA OGLALA was renamed as SHANNON COUNTY in 2015
#     - VIRGINIA BEDFPRD CITY was merged with Bedford county in 2013

# %%
pop_0010_cleaned["COUNTY"] = pop_0010_cleaned["COUNTY"].replace(
    "LASALLE PARISH", "LA SALLE PARISH"
)  # Change name
print((pop_0010_cleaned["COUNTY"] == "LA SALLE PARISH").sum())

# %%
pop_0020 = pd.merge(
    pop_0010_cleaned, pop_1020_cleaned, how="outer", on=["STATE_NAME", "COUNTY"]
)
pop_0020_cleaned = pop_0020.rename(columns={"COUNTY": "COUNTY_NAME"})
pop_0020_cleaned.head(20)

# %% [markdown]
# #### 3. Merging data : FIPS(COUTY CODE) + POPULATION(2000 ~ 2020)

# %%
# ERROR CHECK -> CORRECTION [1] DISTRICT OF COLUMBIA (updated), [2] DOA ANA COUNTY vs DoÒa Ana County -> DONA ANA COUNTY
merge_test = pd.merge(
    fips_cleaned,
    pop_0020_cleaned,
    on=["STATE_NAME", "COUNTY_NAME"],
    how="left",
    indicator=True,
)
print(merge_test["_merge"].value_counts())
merge_test = merge_test[
    (merge_test["_merge"] == "left_only") | (merge_test["_merge"] == "right_only")
]  # | is 'OR'
print(merge_test)

# %%
pop_0020_final = pd.merge(
    fips_cleaned, pop_0020_cleaned, on=["STATE_NAME", "COUNTY_NAME"], how="left"
)
pop_0020_final_0715 = pop_0020_final.rename(
    columns={"COUNTY_NAME": "COUNTY", "COUNTY": "COUNTY_CODE"}
)
pop_0020_final_0715


# %% [markdown]
# #### Groupby
#
# - 2007~2015
# - Reshaping

# %%
columns = ["STATE_NAME", "STATE", "COUNTY", "COUNTY_CODE", "YEAR", "POPULATION"]
reshaped_data = []

for index, row in pop_0020_final_0715.iterrows():
    for year in range(2007, 2016):
        reshaped_data.append(
            [
                row["STATE_NAME"],
                row["STATE"],
                row["COUNTY"],
                row["COUNTY_CODE"],
                year,
                row[str(year)],
            ]
        )

pop_0715_reshaped = pd.DataFrame(reshaped_data, columns=columns)

pop_0715_reshaped.head(20)

# %%
pop_0715_reshaped.to_csv("pop_0715_reshaped.csv", index=False)
print("CSV file saved")
