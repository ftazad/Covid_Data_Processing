import os
import pandas as pd

years = [2020, 2021, 2022, 2023]
data = []

for year in years:
    data_dir = f"JoinedData_NonPR/{year}"
    files = os.listdir(data_dir)
    for idx, file in enumerate(files):
        print(f"Processing {file}")
        df = pd.read_excel(f"{data_dir}/{file}")
        d = [file, df.shape[0]]
        data.append(d)

        # if idx == 0:
        #     break

record_count_df = pd.DataFrame(data, columns=['FileName', 'RecordCount'])
record_count_df.to_excel("JoinedData_NonPR_Record_Count.xlsx")