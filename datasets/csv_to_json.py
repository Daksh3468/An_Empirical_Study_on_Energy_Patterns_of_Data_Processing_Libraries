import pandas as pd
import numpy as np
import json

# Load the CSV
df = pd.read_csv('exam_score.csv')

# Replace NaN with None for proper JSON formatting
df = df.replace({np.nan: None})

# Convert to a list of dictionaries
data = df.to_dict(orient='records')

# Write to JSON
with open('exam_score.json', 'w') as f:
    json.dump(data, f, indent=4)
