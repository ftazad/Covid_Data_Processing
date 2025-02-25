import os
import pandas as pd

combined_cases = []

years = [2020, 2021, 2022, 2023]
for year in years: 
    case_file = f"DownloadedFiles_Cases/us-counties-{year}.csv"
    case_df = pd.read_csv(case_file,dtype={'fips': 'Int64'})
    combined_cases.append(case_df)

combined_case_df = pd.concat(combined_cases)
combined_case_df.loc[combined_case_df['county'] == 'New York City', 'fips'] = 36061
cc_df_nn_fips = combined_case_df.dropna(subset=['fips'])


static_data_dir = 'StateWiseStaticData_Task2'

states = os.listdir(static_data_dir)

for idx, state in enumerate(states):

    print(f"Processing {state}")

    static_data_file = os.listdir(f"{static_data_dir}/{state}")[0]

    s_df = pd.read_excel(f"{static_data_dir}/{state}/{static_data_file}")
    
    case_comm_merged = pd.merge(cc_df_nn_fips, s_df,
                                left_on=['date', 'fips'],
                                right_on=['date', 'FIPS code'])
    

    f_df = case_comm_merged.drop(columns=['county', 'state', 'fips'], axis=1)

    dest_dir = f"StateWise_Static_Case_Joined_Tast2/{state}"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    f_df.to_excel(f"{dest_dir}/Community_Profile_Report.xlsx", index=False)