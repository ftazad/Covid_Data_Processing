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


static_data_dir = 'StateWiseStaticData'
temporal_data_dir = 'StateWiseTemporalData'

states = os.listdir(temporal_data_dir)

for idx, state in enumerate(states):

    print(f"Processing {state}")

    static_data_file = os.listdir(f"{static_data_dir}/{state}")[0]
    temporal_data_file = os.listdir(f"{temporal_data_dir}/{state}")[0]

    s_df = pd.read_excel(f"{static_data_dir}/{state}/{static_data_file}")
    v_df = pd.read_excel(f"{temporal_data_dir}/{state}/{temporal_data_file}")

    m_d_df = pd.merge(s_df, v_df, 
                    left_on=['date', 'FIPS code'],
                    right_on=['date', 'FIPS code'])
    
    case_comm_merged = pd.merge(cc_df_nn_fips, m_d_df,
                                left_on=['date', 'fips'],
                                right_on=['date', 'FIPS code'])
    

    f_df = case_comm_merged.drop(columns=['county', 'state', 'fips', 'State Abbreviation_y'], axis=1)

    dest_dir = f"StateWise_Temporal_Static_Case_Joined/{state}"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    f_df.to_excel(f"{dest_dir}/Community_Profile_Report.xlsx", index=False)