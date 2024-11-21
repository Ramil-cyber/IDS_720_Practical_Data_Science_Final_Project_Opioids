# import pandas as pd
# opioid_test = pd.read_csv(
#     "https://github.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/raw/refs/heads/main/06_Tests/sample_data_1000_opoidshipment(prescription_b2b).csv"
#     )
# print(opioid_test)

import pandas as pd

# Define the URL for the CSV file
url = "https://github.com/MIDS-at-Duke/opioids-2024-optoid-drug-mortality-group5/raw/refs/heads/main/06_Tests/sample_data_1000_opoidshipment%28prescription_b2b%29.csv"

# Read the CSV file from the URL
opioid_test = pd.read_csv(url)

# Print the DataFrame
print(opioid_test)
