import json
import gzip

def compress_json(input_file,output_file):
    """
    Compress a JSON file using gzip without changing its extension.
    
    :param input_file: Path to the input JSON file.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with gzip.open(output_file, 'wt', encoding='utf-8') as f:
        json.dump(data, f)

# Example usage
compress_json('USCensus1990_main.json','USCensus1990_n.json')
