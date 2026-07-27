from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
import dask.dataframe as pd
import pandas as pds
import time
from clear_cache_util import clear_caches

csv_handler = CSVHandler('Dask_exam_v2022.1.0_itr(30).csv')

def sleep():
    time.sleep(30)

# I/O functions - READ
@measure_energy(handler=csv_handler)
def load_csv(path):
    return pd.read_csv(path)

# @measure_energy(handler=csv_handler)
# def load_hdf(path, key):
#     return pd.read_hdf(path, key=key)

@measure_energy(handler=csv_handler)
def load_json(path):
    return pd.read_json(path, orient=str)

# I/O functions - WRITE
@measure_energy(handler=csv_handler)
def save_csv(df, path):
    return df.to_csv(path)

# @measure_energy(handler=csv_handler)
# def save_hdf(df, path, key):
#     return df.to_hdf(path, key=key, mode='w')

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
    def fill_partition(pdf):
        numeric_cols = pdf.select_dtypes(include=['number']).columns.tolist()
        return pdf.fillna({col: val for col in numeric_cols})

    return df.map_partitions(fill_partition)


@measure_energy(handler=csv_handler)
def replace(df, cname, src, dest):
    def replace_partition(pdf):
        if pds.api.types.is_string_dtype(pdf[cname]):
            pdf[cname] = pdf[cname].astype('object')
        pdf[cname] = pdf[cname].replace(src, dest)
        return pdf

    return df.map_partitions(replace_partition)

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

print("Starting Exam Score Dask Process...")
for i in range(30):
    clear_caches()
    df = load_csv('../datasets/exam_score.csv')
    sleep()
    clear_caches()
    df = load_json(path='../datasets/exam_score.json')
    sleep()
    clear_caches()
    # df = load_hdf(path='../datasets/exam_score_dask.h5', key='a')
    # sleep()
    
    save_csv(df, f'df_exam_score_dask{i}.csv')
    sleep()
    save_json(df, f'df_exam_score_dask{i}.json')
    sleep()
    # df = df.compute()
    # for col in df.columns:
    #     if pds.api.types.is_string_dtype(df[col]):
    #         df[col] = df[col].astype(object)
    # save_hdf(df, f'df_exam_score_dask{i}.hdf', key='a')
    # sleep()
    clear_caches()

    print("save done")
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
print("Process complete")
csv_handler.save_data()
