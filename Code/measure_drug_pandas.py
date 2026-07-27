from pickletools import read_uint1
from random import sample
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from clear_cache_util import clear_caches 

csv_handler = CSVHandler('pandas_drug_v1.0.0_itr(30).csv')
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

# @measure_energy(handler=csv_handler)
# def drop_column(df, col_names=[]):
#     df.drop(columns=col_names)

# @measure_energy(handler=csv_handler)
# def remove_duplicates(df):
#     return df.drop_duplicates()

# @measure_energy(handler=csv_handler)
# def merge(df1, df2, on=None):
#     if(on):
#         return pd.merge(df1, df2, on=on)
#     else:
#         return pd.merge(df1, df2)

# @measure_energy(handler=csv_handler)
# def group_by(df, groupby):
#     pass

# # subset 
# @measure_energy(handler=csv_handler)
# def subset(df, subset):
#     return df[subset]

# # sample
# @measure_energy(handler=csv_handler)
# def sample(df, cnt=1000):
#     return df.sample(cnt)

# count, mean, min, max, value_counts, unique, sort values, groupby


print("Starting Drug Pandas Process...")
for i in range(30):
    # Input output functions 
    clear_caches()
    df = load_csv(path='../datasets/drugs.csv')
    sleep()
    df = load_json(path='../datasets/drugs.json')
    sleep()
    # df = load_hdf(path='../datasets/drugs1.h5')
    # sleep()

    save_csv(df, f'df_drug_pandas{i}.csv')
    sleep()
    save_json(df, f'df_drug_pandas{i}.json')
    sleep()
    # save_hdf(df, f'df_drug_pandas{i}.h5', key='a')
    # sleep()

    # --------------------------------------------------

    # Handling missing data
    clear_caches()
    df = pd.read_csv('../datasets/drugs.csv')
    sleep()
    isna(df, cname='review')
    sleep()
    dropna(df)
    sleep()
    fillna(df, val='0')
    sleep()
    replace(df, cname='review', src='?', dest='X')
    sleep()

    # --------------------------------------------------
    # Table operations
    #df = pd.read_csv('../datasets/drugs.csv')
    clear_caches()
    df_samp = pd.read_csv('../datasets/drugs.csv')
    sleep()
    drop(df, cnameArray=['drugName'])
    sleep()
    groupby(df, cname='rating')
    sleep()

    concat_dataframes(df, df_samp)
    sleep()

    sort(df, 'rating')
    sleep()
    merge(df, df_samp)
    sleep()

    # ------------------------------------------
    # Statistical operations
    clear_caches()
    df = pd.read_csv('../datasets/drugs.csv')
    sleep()
    count(df)
    sleep()
    sum(df, 'usefulCount')
    sleep()
    mean(df['rating'])
    sleep()
    min(df['usefulCount'])
    sleep()
    max(df['usefulCount'])
    sleep()
    unique(df['condition'])
    sleep()

    clear_caches()
    print(f"finished {i+1} iterations.")

csv_handler.save_data()
print("Process ended...")

# df = load_csv(path='../datasets/drugs.csv')
# drop_column(df, col_names=['age', 'education', 'occupation'])


# # time.sleep(2)


# remove_duplicates(df_with_dup)
# # time.sleep(2)

# # time.sleep(2)

# SUBSET = ['age', 'workclass', 'education', 'sex', 'race']
# SUBSET_A = ['occupation', 'relationship']
# subset(df, SUBSET)
# # time.sleep(2)

# sample(df, 1000)
# # time.sleep(2)
# sample(df, 10000)
# # time.sleep(2)
# sample(df, 20000)
# # time.sleep(2)

# col = ['capital-gain', 'capital.loss', 'hours.per.week']
# # col = ['capital-gain', 'capital.loss']


