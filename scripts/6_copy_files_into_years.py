import os
import shutil
from datetime import datetime

directory = "CommonColumnExtract_BackFilled"
files = os.listdir(directory)

for idx, file in enumerate(files):

    print(f"{file}")
    
    file_date = file.split('_')[6]
    try:
        iso_date = datetime.strptime(file_date, "%Y%m%d").date().isoformat()
        year = datetime.strptime(file_date, "%Y%m%d").date().year
        dest = f"CommonColumnExtract_BackFilled_YearSplit/{year}"

        if not os.path.exists(dest):
            os.makedirs(dest)
        
        if os.path.exists(dest):
            shutil.copy(f"{directory}/{file}", dest)

    except Exception as e:
        print(f"Invalid_Date: {file}")
        raise e