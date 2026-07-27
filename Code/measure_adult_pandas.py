from pickletools import read_uint1
from random import sample
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from clear_cache_util import clear_caches 

csv_handler = CSVHandler('pandas_adult_v1.0.0_itr(30).csv')
import time
import pandas as pd

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
    return pd.read_json(path)

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
        return pd.merge(df1, df2, on=on)
    else:
        return pd.merge(df1, df2)

@measure_energy(handler=csv_handler)
def sort(df, cname):
    return df.sort_values(by=[cname])

# def transpose(df):
#     return df.transpose()

@measure_energy(handler=csv_handler)
def concat_dataframes(df1, df2):
    return pd.concat([df1, df2])

###--------------------------------------------###
# Statistical Operations
# min, max, mean, count, unique, correlation

# count 
@measure_energy(handler=csv_handler)
def count(df):
    return df.count()

# sum
@measure_energy(handler=csv_handler)
def sum(df, cname):
    return df[cname].sum()

# mean
@measure_energy(handler=csv_handler)
def mean(df):
    return df.mean()

# min
@measure_energy(handler=csv_handler)
def min(df):
    return df.min()
# max
@measure_energy(handler=csv_handler)
def max(df):
    return df.max()

# unique
@measure_energy(handler=csv_handler)
def unique(df):
    return df.unique()

print("Starting Adult Pandas Process...")
for i in range(30):
    # Input output functions 
    clear_caches()
    df = load_csv(path='../datasets/adult.csv')
    sleep()
    df = load_json(path='../datasets/adult.json')
    sleep()
    # df = load_hdf(path='../datasets/adult1.h5')
    # sleep()

    save_csv(df, f'df_adult_pandas_{i}.csv')
    sleep()
    save_json(df, f'df_adult_pandas_{i}.json')
    sleep()
    # save_hdf(df, f'df_adult_pandas_{i}.h5', key='a')
    # sleep()
# --------------------------------------------------

    # Handling missing data
    clear_caches()
    df = pd.read_csv('../datasets/adult.csv')
    sleep()
    isna(df, cname='workclass')
    sleep()
    dropna(df)
    sleep()
    fillna(df, val='0')
    sleep()
    replace(df, cname='workclass', src='?', dest='X')

# --------------------------------------------------
    # Table operations
    clear_caches()
    df = pd.read_csv('../datasets/adult.csv')
    df_samp = pd.read_csv('../datasets/adult.csv')
    sleep()
    drop(df, cnameArray=['age', 'education'])
    sleep()
    groupby(df, cname='workclass')
    sleep()

    SAMPLE_SIZE = 20000
    df_samp = df.sample(SAMPLE_SIZE)
    sleep()
    concat_dataframes(df, df_samp)
    sleep()
    
    sort(df, 'age')
    sleep()
    merge(df, df_samp)
    sleep()

# ------------------------------------------
# Statistical operations
    clear_caches()
    df = pd.read_csv('../datasets/adult.csv')
    sleep()
    count(df)
    sleep()
    sum(df, 'capital-gain')
    sleep()
    mean(df['age'])
    sleep()
    min(df['capital-gain'])
    sleep()
    max(df['capital-gain'])
    sleep()
    unique(df['age'])
    sleep()

    clear_caches()
    print(f"finished {i+1} iterations.")

csv_handler.save_data()
print("Process ended...")
