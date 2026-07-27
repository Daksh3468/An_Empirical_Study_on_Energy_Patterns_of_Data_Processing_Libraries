import json

def count_json_records(file_path):
    count = 0
    with open(file_path, 'r') as f:
        data = json.load(f)
        count = len(data)
    return count

print("Number of records:", count_json_records('USCensus1990.json'))
