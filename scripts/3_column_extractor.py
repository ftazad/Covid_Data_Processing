import os
import pandas as pd
directory = "C:/Users/sandy/Documents/T/CLabProjects/COVID19Data/ProcessedFiles"
files = os.listdir(directory)

for idx, file in enumerate(files):
    df = pd.read_excel(f"ProcessedFiles/{file}")
    columns = df.columns.to_list()
    if idx == 0:
        common_columns = set(columns)
    else:
        common_columns = common_columns & set(columns)
    print(f"{idx}: Processing {file}")


with open ('extracted_files_common_columns.txt', 'w') as f:
    for c in common_columns:
        f.write(f"{c}\n")

print(f"No of unique headers: {len(common_columns)}")

common_columns_list = list(common_columns)


for idx, file in enumerate(files):
    df = pd.read_excel(f"ProcessedFiles/{file}", usecols=common_columns_list)
    df.to_excel(f"CommonColumnExtract/CommonCols_{file}", sheet_name='Counties', index=False)

    print(f"{idx}: Extracted Common Columns for {file}")
