# Updated Code with Smaller Chunk Size and Sequential Processing:
# Here’s the modified version of your code that uses 10 million rows per chunk and processes the file sequentially
# Note that this now includes the GC to try and reduce the linear increase in runtimes for each chunk. 
#  The time without gc ran for 762 minutes, so this should run faster hopefully
# chunk size is 10000000, optimized for 32GB ram, though it needs to be checked to see if GC improved this and can handle larger chunk sizes
# OUTPUT RESULTS: 60 distinct state list

#count of rows from the original tsv should be this:
# I also verify the output state specific files sum to 759,908,394, and the original tsv file was 759,908,393. I think it is off by 1 because of the row header
state_counts = [
    ("AA", 3),
    ("AE", 15),
    ("AK", 1592736),
    ("AL", 17018693),
    ("AP", 1722),
    ("AR", 9132510),
    ("AS", 1296),
    ("AZ", 15208382),
    ("CA", 58303615),
    ("CO", 12071646),
    ("CT", 7630843),
    ("DC", 672652),
    ("DE", 2461249),
    ("FL", 46733822),
    ("GA", 27184152),
    ("GU", 26871),
    ("HI", 2169795),
    ("IA", 6576829),
    ("ID", 3930467),
    ("IL", 31803400),
    ("IN", 19868434),
    ("KS", 7481557),
    ("KY", 14976833),
    ("LA", 12162850),
    ("MA", 12428029),
    ("MD", 12612161),
    ("ME", 3763923),
    ("MI", 24614380),
    ("MN", 9989139),
    ("MO", 17290906),
    ("MP", 8731),
    ("MS", 10242405),
    ("MT", 3022745),
    ("NC", 27391710),
    ("ND", 1602563),
    ("NE", 4174718),
    ("NH", 3405079),
    ("NJ", 18182696),
    ("NM", 4209249),
    ("NV", 6193792),
    ("NY", 38782438),
    ("OH", 37950242),
    ("OK", 12579175),
    ("OR", 10118547),
    ("PA", 32841023),
    ("PR", 1010559),
    ("PW", 137),
    ("RI", 2277760),
    ("SC", 12163348),
    ("SD", 1804095),
    ("TN", 25133974),
    ("TX", 55886524),
    ("UT", 8036219),
    ("VA", 16695504),
    ("VI", 44844),
    ("VT", 1794932),
    ("WA", 16639628),
    ("WI", 21926619),
    ("WV", 6569636),
    ("WY", 1510592)
]



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

    # After all chunks are processed, print out distinct 2-letter states and their row counts
    print("\nDistinct 2-letter states and their row counts:")
    for state, count in sorted(all_state_counts.items()):
        if len(state) == 2:  # Filter out non-2-letter state codes
            print(f"{state}: {count}")

# Call the process_file function to start the processing with the correct encoding
process_file(encoding='ISO-8859-1')  # Replace with the encoding that worked for you
