import os
import numpy as np
import pandas as pd

pd.set_option('mode.copy_on_write', True)

# Define paths
input_folder = 'Sort_By_State_2'
output_folder = 'shipping_by_state'

# List all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Process each file
for file_name in csv_files:
    # Construct full file paths
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name)
    
    # Read the CSV file in chunks
    AK = pd.read_csv(
        input_file_path,
        chunksize=50_000_000,
        usecols=[
            'BUYER_STATE',
            'BUYER_COUNTY',
            'MME_Conversion_Factor',
            'DRUG_NAME',
            'TRANSACTION_DATE',
            'CALC_BASE_WT_IN_GM'
        ])
    
    pieces = []
    for idx, a in enumerate(AK):
        # Process the chunk
        a['TRANSACTION_DATE'] = pd.to_datetime(a['TRANSACTION_DATE'])
        a['year'] = a['TRANSACTION_DATE'].dt.year
        a = a[a['DRUG_NAME'].isin([
            'HYDROCODONE',
            'OXYCODONE',
            'MORPHINE',
            'FENTANYL',
            'BUPRENORPHINE',
            'CODEINE',
            'HYDROMORPHONE',
            'METHADONE',
            'MEPERIDINE',
            'OXYMORPHONE',
            'TAPENTADOL',
            'OPIUM, POWDERED',
            'LEVORPHANOL',
            'DIHYDROCODEINE',
            'HEROIN',
            # "Naloxone (Narcan, Evzio)",       Opioids Used for Overdose Treatment
            # "Naltrexone (Vivitrol, ReVia)"    Opioids Used for Overdose Treatment
            ''])]
        a['strength'] = a['CALC_BASE_WT_IN_GM'] * a['MME_Conversion_Factor']
        
        # Select relevant columns
        a = a[['year', 'strength', 'BUYER_COUNTY', 'BUYER_STATE']]
        
        # Group by and sum
        collapsed = a.groupby(['year', 'BUYER_COUNTY', 'BUYER_STATE'], as_index=False).sum()
        pieces.append(collapsed)
        
        print(f"Processed chunk {idx + 1} from {file_name}")
    
    # Concatenate all processed pieces into a single DataFrame
    final_df = pd.concat(pieces, ignore_index=True)
    
    # Save the final dataset to the output folder
    final_df.to_csv(output_file_path, index=False)
    
    print(f"Processed data saved to {output_file_path}")
