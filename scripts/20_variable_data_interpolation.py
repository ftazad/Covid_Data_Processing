import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

src_dir = 'StateWiseVariableData'

states = os.listdir(src_dir)

interpolable_elements = [
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
    'Number of days of downward case trajectory',
    'Median test latency - last 7 days',
    '% tests resulted in 3 or fewer days - last 7 days',
    'Testing latency - absolute change',
    '% tests resulted in 3 or fewer days - absolute change'
]

exception = []


for idx, state in enumerate(states):

    print(f"Processing: {state}")
    
    file = os.listdir(f"{src_dir}/{state}")[0]
    file_df = pd.read_excel(f"{src_dir}/{state}/{file}")
    fips_codes = file_df['FIPS code'].unique().tolist()

    all_fips_data = []

    for fips in fips_codes:
        # if fips % 1000 == 0:
        #     continue
        fips_df = file_df[file_df['FIPS code'] == fips].copy()
        fips_df['date'] = pd.to_datetime(fips_df['date'])
        fips_df.set_index('date', inplace=True)
        full_date_range = pd.date_range(start=fips_df.index.min(), end=fips_df.index.max(), freq='D')
        fips_df = fips_df.reindex(full_date_range)
        fips_df['FIPS code'] = fips_df['FIPS code'].fillna(fips)
        fips_df['FIPS code'] = fips_df['FIPS code'].astype(int)
        fips_df['State Abbreviation'] = fips_df['State Abbreviation'].fillna(state)
        fips_df.index.name = 'date'

        for element in interpolable_elements:
            x = np.arange(len(fips_df))
            y = fips_df[element].values
            mask = ~np.isnan(y)
            try:
                spline_func = interp1d(x[mask], y[mask], kind='cubic', fill_value='extrapolate')
                fips_df[element] = spline_func(x)
            except ValueError:
                exception.append([state, fips, element])
                # print(f"Skipped Interpolation: {state}, {fips}, {element}")
        
        all_fips_data.append(fips_df)
    

    dest_dir = f"StateWiseVariableDataInterpolated/{state}"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    reconstructed_df = pd.concat(all_fips_data)
    reconstructed_df.reset_index(inplace=True)
    reconstructed_df['date'] = reconstructed_df['date'].dt.strftime('%Y-%m-%d')
    reconstructed_df.to_excel(f"{dest_dir}/{file}", index=False)

    exception_df = pd.DataFrame(exception, columns=['state', 'fips', 'element'])
    exception_df.to_excel("VariableDataInterpolationException.xlsx", index=False)

    # if idx == 0:
    #     break