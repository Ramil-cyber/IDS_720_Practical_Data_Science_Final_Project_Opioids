import pandas as pd
import os
import time
import gc  # Importing the garbage collection module

def create_unique_output_dir(base_dir="Sort_By_State"):
    """
    This function will create a unique output directory by appending a number to the base directory name.
    If the folder already exists, it will increment the number until it finds an available name.
    """
    output_dir = base_dir
    i = 2
    while os.path.exists(output_dir):
        output_dir = f"{base_dir}_{i}"
        i += 1
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory is: {output_dir}")
    return output_dir

def process_chunk(chunk_number, chunk_size=10000000, encoding='ISO-8859-1', output_dir="Sort_By_State"):
    # Calculate the number of rows to skip for this chunk
    skip = (chunk_number - 1) * chunk_size  # Skip rows based on chunk_number

    # Start time for processing the chunk
    start_time = time.time()

    # Reading the chunk and processing it with a specified encoding
    chunk = pd.read_csv(
        "C:/Users/Yirang/PYTHON/arcos_all/arcos_all.tsv",  # Full path for clarity
        sep="\t",
        skiprows=range(1, skip+1),  # Skip the first `skip` rows (header is at line 0)
        nrows=chunk_size,           # Read `chunk_size` rows
        header=0,                   # Ensure header is read
        encoding=encoding           # Use the identified encoding
    )

    # Group by 'BUYER_STATE' and process each state in the current chunk
    state_counts = {}
    grouped = chunk.groupby('BUYER_STATE')

    # For each group (state), save it to a separate CSV file and count rows
    for state, group in grouped:
        file_path = os.path.join(output_dir, f"{state}.csv")
        group.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
        
        # Count the number of rows for each state
        state_counts[state] = state_counts.get(state, 0) + len(group)

    # End time for processing the chunk
    end_time = time.time()

    # Log processing time for the chunk
    print(f"Processed chunk {chunk_number}, wrote groups to files.")
    print(f"Time taken for chunk {chunk_number}: {end_time - start_time:.2f} seconds.")
    
    # Free up memory after each chunk
    del chunk  # Delete the chunk DataFrame to free memory
    gc.collect()  # Run garbage collection to release memory

    return state_counts

def process_file(encoding='ISO-8859-1'):
    chunk_number = 1
    end_of_file = False

    # Determine the total number of rows in the file once before starting
    with open("C:/Users/Yirang/PYTHON/arcos_all/arcos_all.tsv", "r", encoding=encoding) as f:
        total_rows = sum(1 for _ in f) - 1  # Subtract header row
    print(f"Total number of rows in the file: {total_rows}")

    # Create a unique output directory to avoid overwriting existing CSVs
    output_dir = create_unique_output_dir(base_dir="Sort_By_State")

    # Dictionary to keep track of all state counts across chunks
    all_state_counts = {}

    # Process the file in chunks
    while not end_of_file:
        print(f"Processing chunk {chunk_number}...")

        # Process the current chunk and get state counts
        chunk_state_counts = process_chunk(chunk_number, encoding=encoding, output_dir=output_dir)

        # Update the overall state counts
        for state, count in chunk_state_counts.items():
            all_state_counts[state] = all_state_counts.get(state, 0) + count

        # Update the condition to check if all rows are processed
        rows_processed = chunk_number * 10000000  # Adjust based on chunk size (10 million)
        if rows_processed >= total_rows:
            end_of_file = True
            print("All data has been processed.")
        else:
            chunk_number += 1

    # Print out distinct 2-letter states and their row counts
    print("\nDistinct 2-letter states and their row counts:")
    for state, count in sorted(all_state_counts.items()):
        if len(state) == 2:  # Filter out non-2-letter state codes
            print(f"{state}: {count}")

# Call the process_file function to start the processing with the correct encoding
process_file(encoding='ISO-8859-1')
