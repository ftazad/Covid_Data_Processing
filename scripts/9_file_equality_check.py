import os
import pandas as pd

dir = "CommonColumnExtract_BackFilled"

files = os.listdir(dir)

for i in range(1, len(files)):
    curr_file = files[i]
    prev_file = files[i-1]

    curr_df = pd.read_excel(f"{dir}/{curr_file}")
    prev_df = pd.read_excel(f"{dir}/{prev_file}")

    if curr_df.equals(prev_df):
        print(f"{prev_file} and {curr_file} are same")