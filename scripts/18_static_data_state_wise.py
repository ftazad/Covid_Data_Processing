import os
import pandas as pd

years = [2020, 2021, 2022, 2023]
combined_data = []

for year in years:

    source_dir = f"YearWiseStaticData/{year}"
    files = os.listdir(source_dir)

    for file in files:
        df = pd.read_excel(f"{source_dir}/{file}")
        combined_data.append(df)
        print(f"Input: {file}, RecordCount: {df.shape[0]}")

combined_df = pd.concat(combined_data)

states = combined_df['State Abbreviation'].unique().tolist()

for state in states:

    state_df = combined_df[combined_df['State Abbreviation'] == state]

    dest_dir = f"StateWiseStaticData/{state}"

    if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    
    state_df.to_excel(f"{dest_dir}/Community_Profile_Report.xlsx", index=False)

    print(f"State: {state}, RecordCount: {state_df.shape[0]}")