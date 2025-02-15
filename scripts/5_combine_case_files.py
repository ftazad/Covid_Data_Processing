import os
import pandas as pd
from datetime import datetime

directory = "C:/Users/sandy/Documents/T/CLabProjects/COVID19Data/DownloadedFiles_Cases"
csse_files = os.listdir(directory)
li = []

for idx, file in enumerate(csse_files):
    df = pd.read_csv(f"DownloadedFiles_Cases/{file}")
    print(f"File Name: {file}, Record Count: {df.shape[0]}")
    li.append(df)

combined_case_df = pd.concat(li)
print(combined_case_df.shape)
