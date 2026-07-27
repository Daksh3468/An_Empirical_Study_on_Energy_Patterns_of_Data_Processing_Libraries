import pandas as pd
import numpy as np
import os

def remove_outliers_median(group, outlier_cols):
    for col in outlier_cols:
        if col in group.columns:
            median = group[col].median()
            mad = np.median(np.abs(group[col] - median))

            # Skip low-variance data
            if mad == 0 or mad / median < 0.05:
                continue

            threshold = 3  # MAD multiplier
            lower = median - threshold * mad
            upper = median + threshold * mad

            # Additional: Only remove if the suspected outlier deviates greatly (>40% of median)
            deviation_threshold = 0.4  # 40%
            group = group[
                ~(((group[col] < lower) | (group[col] > upper)) & 
                  (np.abs(group[col] - median) > deviation_threshold * median))
            ]
    return group

def csv_summary(filename, output_dir="summary_files"):
    df = pd.read_csv(filename, delimiter=';')

    outlier_cols = ['package_0', 'dram_0']
    has_tag = 'tag' in df.columns

    if has_tag:
        filtered_df = df.groupby('tag', group_keys=False).apply(remove_outliers_median, outlier_cols=outlier_cols)
    else:
        print("⚠️ No 'tag' column found. Applying outlier removal to entire dataset.")
        filtered_df = remove_outliers_median(df, outlier_cols=outlier_cols)

    selected_cols = ['duration', 'package_0', 'dram_0', 'core_0']

    if has_tag:
        avg_df = filtered_df.groupby('tag')[selected_cols].mean().reset_index()
    else:
        avg_df = filtered_df[selected_cols].mean().to_frame().T

    desired_tag_order = ['load_csv', 'load_json','load_hdf','save_csv','save_json','save_hdf','isna','dropna','fillna','replace','drop','groupby','concat_dataframes','sort','merge','count','sum','mean','min','max','unique']
    if has_tag:
        avg_df['tag'] = pd.Categorical(avg_df['tag'], categories=desired_tag_order, ordered=True)
        avg_df = avg_df.sort_values('tag')
    os.makedirs(output_dir, exist_ok=True)

    # Create output filename in the new directory
    base_name = os.path.basename(filename)  # e.g., 'pandas_adult.csv'
    output_file = os.path.join(output_dir, base_name.replace('.csv', '_summary.csv'))
    
    avg_df.to_csv(output_file, index=False)
    print(f"✅ Outlier-removed summary saved to '{output_file}'")


    print(f"✅ Outlier-removed (MAD-based with deviation check) energy summary saved to '{output_file}'")

# ======== Call function below ========

if __name__ == "__main__":
    file_array = [
    'pandas_census.csv',
    'pandas_census-n.csv'
    # 'dask_adult.csv',
    # 'dask_bank.csv',
    # 'dask_drug.csv',
    # 'dask_exam.csv',
    # 'dask_water.csv'
    # 'pandas_adult-1.csv',
    # 'pandas_bank-1.csv',
    # 'pandas_drug-1.csv',
    # 'pandas_exam_score-1.csv',
    # 'pandas_water-1.csv',
    # 'pandas_adult-2.csv',
    # 'pandas_bank-2.csv',
    # 'pandas_drug-2.csv',
    # 'pandas_exam_score-2.csv',
    # 'pandas_water-2.csv',
    # 'vaex_adult.csv',
    # 'vaex_bank.csv',
    # 'vaex_drug.csv',
    # 'vaex_exam.csv',
    # 'vaex_water.csv',
    # 'vaex_adult-1.csv',
    # 'vaex_bank-1.csv',
    # 'vaex_drug-1.csv',
    # 'vaex_exam-1.csv',
    # 'vaex_water-1.csv',
    # 'vaex_adult-2.csv',
    # 'vaex_bank-2.csv',
    # 'vaex_drug-2.csv',
    # 'vaex_exam-2.csv',
    # 'vaex_water-2.csv'
    ]
    for file_name in file_array:
        input_file = file_name.strip()
        csv_summary(input_file)
