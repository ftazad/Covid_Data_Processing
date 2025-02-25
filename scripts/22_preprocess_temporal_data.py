# Source Dir: CommonColumnExtract
# Goal: 
#   1. Remove PR, AK, NH states and any FIPS ending with 000
#   2. Select only indicator and temporal columns
#   3. Fill NaN values to 0
# Destination Dir: Temporal_Updated_OrgSeq

import os
import pandas as pd

src_dir = 'CommonColumnExtract'
dest_dir = 'Temporal_Updated_OrgSeq'

k_cols = [
    'FIPS code',
    'State Abbreviation'
]

t_cols_div7 = [
    'Cases as a percent of national total - last 7 days',
    'Cases - last 7 days',
    'Cases per 100k - last 7 days',
    'Deaths - last 7 days',
    'Deaths per 100k - last 7 days',
    'Cases - % change',
    'Deaths - % change',
    'Cases as a percent of national total - previous 7 days',
    'Cases - previous 7 days',
    'Cases per 100k - previous 7 days',
    'Deaths - previous 7 days',
    'Deaths per 100k - previous 7 days',
    'Cumulative cases',
    'Cumulative deaths',
    'Median test latency - last 7 days',
    '% tests resulted in 3 or fewer days - last 7 days',
    'Testing latency - absolute change',
    '% tests resulted in 3 or fewer days - absolute change'
]

t_cols_div1 = [
    'Number of days of downward case trajectory'
]

appl_cols = k_cols + t_cols_div7 + t_cols_div1

files = os.listdir(src_dir)

for idx, file in enumerate(files):

    print(f"{idx} Processing {file}")

    df = pd.read_excel(f"{src_dir}/{file}")

    df = df[df['State Abbreviation'] != 'PR']
    df = df[df['State Abbreviation'] != 'AK']
    df = df[df['State Abbreviation'] != 'NH']
    df = df[(df['FIPS code'] % 1000) != 0]

    t_df = df[appl_cols]
    t_df = t_df.fillna(0)

    t_df[t_cols_div7] = t_df[t_cols_div7]/7

    f_name = '_'.join(file.split('_')[3:])

    t_df.to_excel(f"{dest_dir}/Temporal_{f_name}", index=False)

    # if idx == 0:
    #     break

