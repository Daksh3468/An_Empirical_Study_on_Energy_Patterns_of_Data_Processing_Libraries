from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import time
import pandas as pd
from clear_cache_util import clear_caches 

csv_handler = CSVHandler('pandas_water_v1.0.0_itr(30).csv')

def sleep():
    time.sleep(30)

# I/O functions - READ
@measure_energy(handler=csv_handler)
def load_csv(path):
    return pd.read_csv(path)

# @measure_energy(handler=csv_handler)
# def load_hdf(path):
#     return pd.read_hdf(path)

@measure_energy(handler=csv_handler)
def load_json(path):
    return pd.read_json(path, orient="records", lines=True)

# I/O functions - WRITE
@measure_energy(handler=csv_handler)
def save_csv(df, path):
    return df.to_csv(path)

# @measure_energy(handler=csv_handler)
# def save_hdf(df, path, key):
#     return df.to_hdf(path, key=key)

@measure_energy(handler=csv_handler)
def save_json(df, path):
    return df.to_json(path)

# Handling missing data
@measure_energy(handler=csv_handler)
def isna(df, cname):
    return df[cname].isna()

@measure_energy(handler=csv_handler)
def dropna(df):
    return df.dropna()

@measure_energy(handler=csv_handler)
def fillna(df, val):
    return df.fillna(val)

@measure_energy(handler=csv_handler)
def replace(df, cname, src, dest):
    if src is None:
        return df[cname].fillna(dest)
    return df[cname].replace(src, dest)

# Table operations
@measure_energy(handler=csv_handler)
def drop(df, cnameArray):
    return df.drop(columns=cnameArray)

@measure_energy(handler=csv_handler)
def groupby(df, cname):
    return df.groupby(cname)

@measure_energy(handler=csv_handler)
def merge(df1, df2, on=None):
    return pd.merge(df1, df2, on=on) if on else pd.merge(df1, df2)

@measure_energy(handler=csv_handler)
def sort(df, cname):
    return df.sort_values(by=[cname])

@measure_energy(handler=csv_handler)
def concat_dataframes(df1, df2):
    return pd.concat([df1, df2])

# Statistical operations
@measure_energy(handler=csv_handler)
def count(df):
    return df.count()

@measure_energy(handler=csv_handler)
def sum(df, cname):
    return df[cname].sum()

@measure_energy(handler=csv_handler)
def mean(df):
    return df.mean()

@measure_energy(handler=csv_handler)
def min(df):
    return df.min()

@measure_energy(handler=csv_handler)
def max(df):
    return df.max()

@measure_energy(handler=csv_handler)
def unique(df):
    return df.unique()

print("Starting Water Potability Pandas Process...")
for i in range(30):
    # I/O
    clear_caches()
    df = load_csv('../datasets/water_potability.csv')
    sleep()
    df = load_json('../datasets/water_potability.json')
    sleep()
    # df = load_hdf('../datasets/water_potability.h5')
    # sleep()

    save_csv(df, f'df_water_pandas_{i}.csv')
    sleep()
    save_json(df, f'df_water_pandas_{i}.json')
    sleep()
    # save_hdf(df, f'df_water_pandas_{i}.h5', key='a')
    # sleep()

    # Missing data
    clear_caches()
    df = pd.read_csv('../datasets/water_potability.csv')
    sleep()
    isna(df, cname='ph')
    sleep()
    dropna(df)
    sleep()
    fillna(df, val=0)
    sleep()
    replace(df, cname='ph', src=None, dest=7.0)

    # Table operations
    clear_caches()
    df = pd.read_csv('../datasets/water_potability.csv')
    df_samp = pd.read_csv('../datasets/water_potability.csv')
    sleep()
    drop(df, cnameArray=['ph', 'Solids'])
    sleep()
    groupby(df, cname='Potability')
    sleep()
    concat_dataframes(df, df_samp)
    sleep()
    sort(df, 'Turbidity')
    sleep()
    merge(df, df_samp)
    sleep()

    # Statistical operations
    clear_caches()
    df = pd.read_csv('../datasets/water_potability.csv')
    sleep()
    count(df)
    sleep()
    sum(df, 'Hardness')
    sleep()
    mean(df['Conductivity'])
    sleep()
    min(df['Turbidity'])
    sleep()
    max(df['Turbidity'])
    sleep()
    unique(df['Potability'])
    sleep()

    clear_caches()
    print(f"Finished iteration {i+1}")

csv_handler.save_data()
print("Process complete.")
