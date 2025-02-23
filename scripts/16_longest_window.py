import os
from datetime import datetime, timedelta
import pandas as pd

file_dir = 'CommonColumnExtract'
files = os.listdir(file_dir)

file_dates = []

for idx, file in enumerate(files):   
    file_date = file.split('_')[6]
    try:
        iso_date = datetime.strptime(file_date, "%Y%m%d").date().isoformat()
    except Exception as e:
        print(f"Invalid_Date: {file}")
        raise e
    
    file_dates.append(iso_date)

file_dates.sort()

date_df = pd.DataFrame(file_dates, columns=['date'])
date_df.to_excel("file_dates.xlsx", index=False)