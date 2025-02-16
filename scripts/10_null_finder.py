import os
import pandas as pd


info = []
for year in [2020, 2021, 2022, 2023]:

    # data_dir = f"JoinedData/{year}"
    data_dir = f"JoinedData_NonPR/{year}"

    files = os.listdir(data_dir)
    for file in files:
        print(f"Processing File: {file}")
        file_path = f"{data_dir}/{file}"
        df = pd.read_excel(file_path)
        columns = df.columns.to_list()
        for col in columns:
            null_count = int(df[col].isna().sum())
            if null_count > 0:
                col_det = [file, col, null_count]
                info.append(col_det)

info_df = pd.DataFrame(info, columns=['FileName', 'ColumnName', 'NullCount'])
info_df.to_excel("JoinedData_NonPR_Null_Count.xlsx")