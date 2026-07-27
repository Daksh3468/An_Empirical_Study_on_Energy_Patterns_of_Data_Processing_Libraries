import json

# File paths (update with actual file paths)
input_file = "USCensus1990_main.json"  # Original large JSON file
output_file = "USCensus1990.json"  # Output JSON file

# Read the JSON file
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)  # Assuming the file contains a list of objects

# Extract the first 10 lakh records
subset_data = data[:1_700_000]

# Write to a new JSON file in the same format
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(subset_data, f, indent=4)

print(f"First 10 lakh records saved to {output_file}")
