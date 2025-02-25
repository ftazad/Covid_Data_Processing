import os
from datetime import datetime
import pandas as pd

src_dir = "Temporal_Updated_Backfilled"
files = os.listdir(src_dir)

for idx, file in enumerate(files):

    print(f"Processing: {file}")
    
    file_date = file.split('_')[4]
    try:
        iso_date = datetime.strptime(file_date, "%Y%m%d").date().isoformat()

        year = datetime.strptime(file_date, "%Y%m%d").date().year
        month = datetime.strptime(file_date, "%Y%m%d").date().month
        day = datetime.strptime(file_date, "%Y%m%d").date().day
        
        cur_dt_fmt = f"{year}-{month:02}-{day:02}"

        df = pd.read_excel(f"{src_dir}/{file}")
        df.insert(0, "date", cur_dt_fmt)

        dest = f"YearWiseTemporalData/{year}"

        if not os.path.exists(dest):
            os.makedirs(dest)
        
        if os.path.exists(dest):
            df.to_excel(f"{dest}/{file}", index=False)

    except Exception as e:
        print(f"Invalid_Date: {file}")
        raise e
    
    # if idx == 0:
    #     break