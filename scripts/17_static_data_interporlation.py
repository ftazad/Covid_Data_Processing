import os
import pandas as pd
from datetime import datetime, timedelta

years = [(2020, '20201217', '20201231'), 
         (2021, '20210101', '20211231'), 
         (2022, '20220101', '20221231'), 
         (2023, '20230101', '20230223')]

# years = [(2020, '20201217', '20201231'), 
#          (2023, '20230101', '20230223')]

for (year, s_dt, e_dt) in years:
    data_dir = f"CommonColumnExtract_YearSplit/{year}"
    files = os.listdir(data_dir)

    for idx, file in enumerate(files):

        print(f"Processing {year} - Source File: {file}")
        data_df = pd.read_excel(f"{data_dir}/{file}")
        static_data = data_df[[
            'County',
            'FIPS code',
            'County type',
            'CBSA',
            'CBSA type',
            'State Abbreviation',
            'FEMA region',
            'Population',
            'Population as a percent of CBSA',
            'Population as a percent of state',
            'Population as a percent of national population',
            'IHE with >5000 full-time enrollment',
            '% Uninsured',
            '% In Poverty',
            '% Over Age 65',
            'Average household size',
            '% Non-Hispanic Black',
            '% Hispanic',
            'SVI score',
            'CCVI score'
        ]]


        cur_dt = datetime.strptime(s_dt, "%Y%m%d").date()
        end_dt = datetime.strptime(e_dt, "%Y%m%d").date()

        while cur_dt <= end_dt:
            cur_dt_fmt = f"{cur_dt.year}-{cur_dt.month:02}-{cur_dt.day:02}"
            file_df = static_data.copy()
            file_df.insert(0, "date", cur_dt_fmt)
            file_name = f"Static_Community_Profile_Report_{cur_dt.year}{cur_dt.month:02}{cur_dt.day:02}_Public.xlsx"
            file_df.to_excel(f"YearWiseStaticData/{year}/{file_name}", index=False)
            del file_df
            print(f"    -> Created: {file_name}")
            
            cur_dt= cur_dt + timedelta(days=1)

        if idx == 0:
            break
        
