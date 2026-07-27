import time
import subprocess
import re
import csv
import os
import dask.dataframe as pd
from pathlib import Path

CSV_FILE = 'dask_adult_perf.csv'

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'function', 'energy_pkg_joules', 'energy_ram_joules', 'status'])

def measure_with_perf(command, function_name):
    try:
        result = subprocess.run(
            ['perf', 'stat', '-e', 'power/energy-pkg/,power/energy-ram/', '-x', ',', '--'] + command,
            capture_output=True, text=True, check=True
        )
        stderr = result.stderr
        pkg_energy = re.search(r'(\d+\.\d+) Joules power/energy-pkg/', stderr)
        ram_energy = re.search(r'(\d+\.\d+) Joules power/energy-ram/', stderr)

        pkg_joules = float(pkg_energy.group(1)) if pkg_energy else 0.0
        ram_joules = float(ram_energy.group(1)) if ram_energy else 0.0
        status = "success"

        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.time(), function_name, pkg_joules, ram_joules, status])
    except subprocess.CalledProcessError as e:
        print(f"Perf failed on {function_name}")
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.time(), function_name, 0.0, 0.0, f"error: {e.returncode}"])
    except Exception as e:
        print(f"Error: {e}")
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.time(), function_name, 0.0, 0.0, f"error: {str(e)}"])

def run_function_with_perf(func_code, func_name):
    temp_file = f'temp_{func_name}.py'
    with open(temp_file, 'w') as f:
        f.write(func_code)
    
    measure_with_perf(['python3', temp_file], func_name)

def sleep():
    time.sleep(30)

init_csv()
print("Starting Dask + Perf Measurement...")

for i in range(20):
    run_function_with_perf(
        f"""import dask.dataframe as pd\ndf = pd.read_csv('../datasets/adult.csv')""",
        f'load_csv_{i}'
    )
    sleep()

    run_function_with_perf(
        f"""import dask.dataframe as pd\ndf = pd.read_json('../datasets/adult.json', orient='records', lines=True)""",
        f'load_json_{i}'
    )
    sleep()

    run_function_with_perf(
        f"""import dask.dataframe as pd\ndf = pd.read_hdf('../datasets/adult_dask.h5', key='a')""",
        f'load_hdf_{i}'
    )
    sleep()

    run_function_with_perf(
        f"""import dask.dataframe as pd\ndf = pd.read_csv('../datasets/adult.csv')\ndf.to_csv('df_adult_dask{i}.csv')""",
        f'save_csv_{i}'
    )
    sleep()

    # Repeat similar structure for save_json, save_hdf, and other operations
    # You can expand this section based on your original loop
    print(f"Finished iteration {i+1}")

print("All done!")
