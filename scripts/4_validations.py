import os
import pandas as pd
from datetime import datetime

directory = "C:/Users/sandy/Documents/T/CLabProjects/COVID19Data/CommonColumnExtract"
files = os.listdir(directory)

for idx, file in enumerate(files):

    # print(f"{idx}: Processing {file}.")
    
    file_date = file.split('_')[6]
    try:
        iso_date = datetime.strptime(file_date, "%Y%m%d").date().isoformat()
    except Exception as e:
        print(f"Invalid_Date: {file}")
        raise e
    
    df = pd.read_excel(f"CommonColumnExtract/{file}")
    print(f"{file}, Count: {df.shape[0]}")

