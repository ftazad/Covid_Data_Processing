import os
import pandas as pd

years = [2020, 2021, 2022, 2023]

for year in years:
    joined_data_dir = f"JoinedData/{year}"
    joined_data_non_pr_dr = f"JoinedData_NonPR/{year}"
    files = os.listdir(joined_data_dir)
    for idx, file in enumerate(files):
        print(f"Processing {file}")
        data_df = pd.read_excel(f"{joined_data_dir}/{file}")
        non_pr_df = data_df[data_df['State Abbreviation'] != 'PR']
        non_pr_df.to_excel(f"{joined_data_non_pr_dr}/{file}", index=False)