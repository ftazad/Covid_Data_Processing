import os
import pandas as pd

file_dir = 'ProcessedFiles'

files = os.listdir(file_dir)

file_column_mapping = []
column_set = set()

for idx, file in enumerate(files):
    
    print(f"{idx} Processing {file}")

    df = pd.read_excel(f"{file_dir}/{file}", nrows=1)
    cols = df.columns.to_list()
    column_set.update(cols)

    for col in cols:
        file_column_mapping.append([file, col])

column_list = list(column_set)
column_list.sort()

map_df = pd.DataFrame(file_column_mapping, columns=['File_name', 'ColumnName'])
super_df = pd.DataFrame(column_list, columns=['ColumnNames'])

map_df.to_excel("downloaded_file_county_tab_column_mapping.xlsx", index=False)
super_df.to_excel("downloaded_files_county_tab_uperset_columns.xlsx", index=False)
