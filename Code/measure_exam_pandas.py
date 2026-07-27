from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import time
import pandas as pd
from clear_cache_util import clear_caches 

csv_handler = CSVHandler('pandas_exam_v1.0.0_itr(30).csv')

def sleep():
    time.sleep(30)

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
    return df.nunique()

print("Starting Exam Score Pandas Process...")
for i in range(30):
    clear_caches()
    df = load_csv(path='../datasets/exam_score.csv')
    sleep()
    df = load_json(path='../datasets/exam_score.json')
    sleep()
    # df = load_hdf(path='../datasets/exam_score.h5')
    # sleep()
    
    save_csv(df, f'df_exam_score{i}.csv')
    sleep()
    save_json(df, f'df_exam_score{i}.json')
    sleep()
    # save_hdf(df, f'df_exam_score{i}.hdf', key='a')
    # sleep()

    clear_caches()
    df = pd.read_csv('../datasets/exam_score.csv')
    sleep()
    isna(df, 'ReadingScore')
    sleep()
    dropna(df)
    sleep()
    fillna(df, 0)
    sleep()
    replace(df, 'Gender', 'female', 'F')
    sleep()

    clear_caches()
    df = pd.read_csv('../datasets/exam_score.csv')
    df_samp = pd.read_csv('../datasets/exam_score.csv')
    sleep()
    drop(df, ['ReadingScore'])
    sleep()
    groupby(df, 'Gender')
    sleep()
    concat_dataframes(df, df_samp)
    sleep()
    sort(df, 'ReadingScore')
    sleep()
    merge(df, df_samp)
    sleep()

    clear_caches()
    df = pd.read_csv('../datasets/exam_score.csv')
    count(df)
    sleep()
    sum(df, 'ReadingScore')
    sleep()
    mean(df['ReadingScore'])
    sleep()
    min(df['ReadingScore'])
    sleep()
    max(df['ReadingScore'])
    sleep()
    unique(df['Gender'])
    sleep()

    clear_caches()
    print(f"Finished iteration {i+1}")
csv_handler.save_data()
print("Process complete")
