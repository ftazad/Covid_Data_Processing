import os
import pandas as pd
directory = "C:/Users/sandy/Documents/T/CLabProjects/COVID19Data/ProcessedFiles"
files = os.listdir(directory)


# with open ('extracted_files_header_delim.txt', 'w') as f:
#     for idx, file in enumerate(files):
#         df = pd.read_excel(f"ProcessedFiles/{file}")
#         columns = df.columns.to_list()
#         columns_str = str(columns)[1:-1]
#         no_columns = len(columns)
#         file_detail = f"{file}, '|', {no_columns}, '|', {columns_str}\n"

#         f.write(file_detail)

#         print(f"{idx}: Processed {file}")


# with open ('extracted_files_common_columns.txt', 'w') as f:
#     for idx, file in enumerate(files):
#         df = pd.read_excel(f"ProcessedFiles/{file}")
#         columns = df.columns.to_list()
#         if idx == 0:
#             common_columns = set(columns)
#         else:
#             common_columns = common_columns & set(columns)
        
#         print(f"{idx}: Processed {file}")

#         # if idx == 5:
#         #     break
    
#     f.write(str(common_columns))



for idx, file in enumerate(files):
    df = pd.read_excel(f"ProcessedFiles/{file}")
    columns = df.columns.to_list()
    if idx == 0:
        common_columns = set(columns)
    else:
        common_columns = common_columns & set(columns)
    
    print(f"{idx}: Processed {file}")

    # if idx == 5:
    #     break

with open ('extracted_files_common_columns.txt', 'w') as f:
    for c in common_columns:
        f.write(f"{c}\n")

print(f"No of unique headers: {len(common_columns)}")
