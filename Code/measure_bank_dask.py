from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import dask.dataframe as ds
import pandas as pd
import time
from clear_cache_util import clear_caches

csv_handler = CSVHandler('Dask_bank_v2022.1.0_itr(30).csv')

def sleep():
    time.sleep(30)

# I/O functions - READ
@measure_energy(handler=csv_handler)
def load_csv(path):
    return ds.read_csv(path)

# @measure_energy(handler=csv_handler)
# def load_hdf(path, key):
#     return ds.read_hdf(path, key=key)

@measure_energy(handler=csv_handler)
def load_json(path):
    return ds.read_json(path, orient=str)

# I/O functions - WRITE
@measure_energy(handler=csv_handler)
def save_csv(df, path):
    return df.to_csv(path)

# @measure_energy(handler=csv_handler)
# def save_hdf(df, path, key):
#     # def convert_string_dtype(pdf):
#     #     for col in pdf.columns:
#     #         # Explicitly check for pandas StringDtype
#     #         if str(pdf[col].dtype) == 'string':
#     #             pdf[col] = pdf[col].astype(object)
#     #     return pdf
    
#     # df = df.map_partitions(convert_string_dtype)
#     return df.to_hdf(path, key=key)

@measure_energy(handler=csv_handler)
def save_json(df, path):
    return df.to_json(path)

###------------------------------------------###

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
    return df[cname].replace(src, dest)

###------------------------------------------###

# Table operations
# drop column
# groupby
# merge 
# transpose
# sort
# concat
@measure_energy(handler=csv_handler)
def drop(df, cnameArray):
    return df.drop(columns=cnameArray)

@measure_energy(handler=csv_handler)
def groupby(df, cname):
    return df.groupby(cname)

@measure_energy(handler=csv_handler)
def merge(df1, df2, on=None):
    if(on):
        return ds.merge(df1, df2, on=on)
    else:
        return ds.merge(df1, df2)

@measure_energy(handler=csv_handler)
def sort(df, cname):
    return df.sort_values(by=[cname])

# def transpose(df):
#     return df.transpose()

@measure_energy(handler=csv_handler)
def concat_dataframes(df1, df2):
    return ds.concat([df1, df2])

###--------------------------------------------###
# Statistical Operations
# min, max, mean, count, unique, correlation

# count 
@measure_energy(handler=csv_handler)
def count(df):
    return df.count().compute()

# sum
@measure_energy(handler=csv_handler)
def sum(df, cname):
    return df[cname].sum().compute()

# mean
@measure_energy(handler=csv_handler)
def mean(df):
    return df.mean().compute()

# min
@measure_energy(handler=csv_handler)
def min(df):
    return df.min().compute()
# max
@measure_energy(handler=csv_handler)
def max(df):
    return df.max().compute()

# unique
@measure_energy(handler=csv_handler)
def unique(df):
    return df.unique().compute()


print("Starting Bank Dask Process...")
for i in range(30):
    clear_caches()
    df = load_csv(path='../datasets/bank.csv')
    sleep()
    clear_caches()
    df = load_json(path='../datasets/bank.json')
    sleep()
    clear_caches()
    # df = load_hdf(path='../datasets/bank_dask.h5', key='a')
    # sleep()
    
    save_csv(df, f'df_bank_dask{i}.csv')
    sleep()
    save_json(df, f'df_bank_dask{i}.json')
    sleep()
    # df = df.compute()
    # for col in df.columns:
    #     if pd.api.types.is_string_dtype(df[col]):
    #         df[col] = df[col].astype(object)
    # save_hdf(df, f'df_bank_dask{i}.hdf', key='a')
    # sleep()
    clear_caches()

    df = ds.read_csv('../datasets/bank.csv', sep=';', quotechar='"')
    sleep()
    isna(df, 'job')
    sleep()
    dropna(df)
    sleep()
    fillna(df, 'N/A')
    sleep()
    replace(df, 'job', 'unknown', 'X')
    sleep()
    clear_caches()

    df = ds.read_csv('../datasets/bank.csv', sep=';', quotechar='"')
    sleep()
    df_samp = ds.read_csv('../datasets/bank.csv', sep=';', quotechar='"')
    sleep()
    drop(df, ['job', 'education'])
    sleep()
    groupby(df, 'job')
    sleep()
    concat_dataframes(df, df_samp)
    sleep()
    sort(df, 'age')
    sleep()
    merge(df, df_samp)
    sleep()
    clear_caches()

    df = ds.read_csv('../datasets/bank.csv', sep=';', quotechar='"')
    count(df)
    sleep()
    sum(df, 'balance')
    sleep()
    mean(df['age'])
    sleep()
    min(df['balance'])
    sleep()
    max(df['balance'])
    sleep()
    unique(df['job'])
    sleep()
    clear_caches()

    print(f"Finished iteration {i+1}")
print("Process complete")
csv_handler.save_data()
