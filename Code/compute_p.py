
from scipy.stats import ranksums
import pandas as pd
from itertools import combinations

seperator = ';'
data = {
    # 'adult': ['dask_adult.csv', 'pandas_adult.csv', 'vaex_adult.csv'],
    # 'drug': ['dask_drug.csv', 'pandas_drug.csv', 'vaex_drug.csv'],
    # 'census': ['dask_census.csv', 'pandas_census.csv', 'vaex_census.csv']
    'census': ['pandas_census.csv','pandasN_census.csv']
}

libraries = ['pandas', 'pandasN']
tags = [
    'load_csv', 'load_json', 'load_hdf', 
    'save_csv', 'save_json', 'save_hdf', 
    'isna', 'dropna', 'fillna', 'replace', 
    'drop', 'groupby', 'concat_dataframes', 
    'sort', 'merge', 'count', 'sum', 'mean', 
    'min', 'max', 'unique'
    ]

def getPValue(list1, list2):
    z, p  = ranksums(list1, list2)
    return z, p

def getValuesForTag(tag, dataset):
    res = []
    for file in data[dataset]:
        df = pd.read_csv(f"{file}", sep=seperator)
        library = file.split('_')[0]
        # print(df.head())
        df = df[df['tag'] == tag]
        df['lib'] = library
        res.append(df)
    return pd.concat(res)

def computePvalues(tag, dataset):
    df = getValuesForTag(tag, dataset)
    res = {'tag': tag}
    for combo in list(combinations(libraries, 2)):
        list1 = df[df['lib'] == combo[0]]
        list2 = df[df['lib'] == combo[1]]
        a = list1['package_0'] + list1['dram_0']
        b = list2['package_0'] + list2['dram_0']
        res[f"p{(combo[0], combo[1])}"] = getPValue(a, b)[1]
    return res


for dataset in data:
    res = []
    for tag in tags:
        temp = computePvalues(tag=tag, dataset=dataset)
        res.append(temp)
    df = pd.DataFrame(res)
    print(df) 
    df.to_csv(f"{dataset}_wilcoxon_ranksum_test_pvalues.csv")
        