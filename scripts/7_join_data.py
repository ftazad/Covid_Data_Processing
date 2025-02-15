import os
import gc
import pandas as pd
from datetime import datetime

years = [2020, 2021, 2022, 2023]

with open('7_join_data_log.txt', 'w') as f:
    for year in years:

        print(f"Processing data of year {year}")
        f.write(f"Processing data of year {year}\n")

        data_file_dir = f"CommonColumnExtract_BackFilled_YearSplit/{year}"
        joined_file_dir = f"JoinedData/{year}"
        case_file = f"DownloadedFiles_Cases/us-counties-{year}.csv"

        # Read case files (using 'fips' as integer)
        # Update the 'fips' code for 'New York City'
        # Drop any rows where 'fips' code is null
        case_df = pd.read_csv(case_file,dtype={'fips': 'Int64'})
        case_df.loc[case_df['county'] == 'New York City', 'fips'] = 36061
        case_df_not_null_fips = case_df.dropna(subset=['fips'])

        set_case_file_fips = set(case_df_not_null_fips['fips'].unique().tolist())

        y_data_files = os.listdir(data_file_dir)

        for idx, data_file in enumerate(y_data_files):

            print(f"  -> Processing File: {data_file}")
            f.write(f"  -> Processing File: {data_file}\n")

            data_df = pd.read_excel(f"{data_file_dir}/{data_file}")
            # Extract date from file name and add it to the dataframe
            date_str = data_file.split('_')[6]
            dt = datetime.strptime(date_str, "%Y%m%d").date()
            date_fmt = f"{dt.year}-{dt.month:02}-{dt.day:02}"
            data_df.insert(0, "date", date_fmt)

            if (data_df['FIPS code'].isna().sum() > 0):
                print("  -> FIPS code column contains null")
                raise Exception
            
            merged_df = pd.merge(case_df_not_null_fips, 
                                data_df, 
                                left_on=['date', 'fips'],
                                right_on=['date', 'FIPS code'])
            
            merged_df.to_excel(f"{joined_file_dir}/{data_file}", index=False)

            f.write(f"   -> DataFile Record Count: {data_df.shape[0]}\n")
            f.write(f"   -> CaseFile Record Count (Not Null FIPS): {case_df_not_null_fips.shape[0]}\n")
            f.write(f"   -> Merged Record Count: {merged_df.shape[0]}\n")

            set_data_file_fips = set(data_df['FIPS code'].unique().tolist())

            f.write(f"   -> FIPS in data file but not in case file:\n")
            f.write(f"   -> {set_data_file_fips - set_case_file_fips}\n")
            
            f.write(f"   -> FIPS in case file but not in data file:\n")
            f.write(f"   -> {set_case_file_fips - set_data_file_fips}\n")
            f.write('\n')
            f.write('\n')
            
            del merged_df
            del data_df
            gc.collect()

            # if idx == 0:
            #     break
        
        del case_df_not_null_fips
        del case_df
        gc.collect()
