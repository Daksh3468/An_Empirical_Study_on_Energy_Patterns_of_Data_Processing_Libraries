import pandas as pd

# File path
file_path = "USCensus1990_main.csv"
output_path = "USCensus1990.csv"

# Read the first 10 lakh rows
chunk_size = 1_700_000  # 10 lakh rows
df = pd.read_csv(file_path, nrows=chunk_size)

# Save to a new CSV file
df.to_csv(output_path, index=False)

# Return the output file path
output_path
