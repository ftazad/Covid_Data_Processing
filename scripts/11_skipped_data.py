import os
import pandas as pd

years = [2020, 2021, 2022, 2023]

for year in years:
    backfilled_data_dir = f"CommonColumnExtract_BackFilled_YearSplit/{year}"
    joined_data_dir = f"JoinedData/{year}"
    skipped_data_dir = f"SkippedData/{year}"

    files = os.listdir(backfilled_data_dir)

    for idx, file in enumerate(files):
        print(f"Processing {file}")
        backfilled_data_df = pd.read_excel(f"{backfilled_data_dir}/{file}")
        joined_data_df = pd.read_excel(f"{joined_data_dir}/{file}")
        joined_data_fips_df = joined_data_df['FIPS code']

        merged = pd.merge(backfilled_data_df, joined_data_fips_df, how='left', on='FIPS code', indicator=True)
        left_only = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)

        left_only.to_excel(f"{skipped_data_dir}/{file}", index=False)

        # if idx == 0:
        #     break



