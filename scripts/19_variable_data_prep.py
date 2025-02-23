import os
import pandas as pd
from datetime import datetime

combined_data = []

years = [2020, 2021, 2022, 2023]

for year in years:
    data_dir = f"CommonColumnExtract_YearSplit/{year}"
    files = os.listdir(data_dir)
    for idx, file in enumerate(files):
        print(f"Processing {year} - Source File: {file}")
        data_df = pd.read_excel(f"{data_dir}/{file}")
        variable_data = data_df[[
            'FIPS code',
            'State Abbreviation',
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
        ]]

        date_str = file.split('_')[6]
        try:
            dt = datetime.strptime(date_str, "%Y%m%d").date()
        except Exception as e:
            print(f"Invalid_Date: {file}")
            raise e
        date_fmt = f"{dt.year}-{dt.month:02}-{dt.day:02}"
        variable_data.insert(0, "date", date_fmt)

        combined_data.append(variable_data)

combined_df = pd.concat(combined_data)

states = combined_df['State Abbreviation'].unique().tolist()

for state in states:

    state_df = combined_df[combined_df['State Abbreviation'] == state]

    dest_dir = f"StateWiseVariableData/{state}"

    if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    
    state_df.to_excel(f"{dest_dir}/Community_Profile_Report.xlsx", index=False)

    print(f"State: {state}, RecordCount: {state_df.shape[0]}")