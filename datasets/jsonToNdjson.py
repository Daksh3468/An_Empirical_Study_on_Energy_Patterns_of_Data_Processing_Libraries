import json

with open('../datasets/drugs.json', 'r') as infile:
    # Disable strict mode to allow unescaped control characters
    data = json.load(infile, strict=False)

with open('../datasets/drugs.ndjson', 'w') as outfile:
    for entry in data:
        json.dump(entry, outfile)
        outfile.write('\n')