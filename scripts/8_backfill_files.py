import os
import shutil
from datetime import datetime, timedelta

src_dir = "CommonColumnExtract"
dst_dir = "CommonColumnExtract_BackFilled"

src_files = os.listdir(src_dir)

available_dates = []

for idx, file in enumerate(src_files):
    file_date = file.split('_')[6]
    try:
        iso_date = datetime.strptime(file_date, "%Y%m%d").date().isoformat()
        available_dates.append(iso_date)
    except Exception as e:
        print(f"Invalid_Date: {file}")
        raise e

sorted_dates = sorted(available_dates)

if (sorted_dates == available_dates):
    first_date = available_dates[0]
    first_date_fmt = ''.join(first_date.split('-'))

    # Copy the first file in the folder
    first_file_name = f"CommonCols_County_Data_Community_Profile_Report_{first_date_fmt}_Public.xlsx"

    shutil.copy(f"{src_dir}/{first_file_name}", f"{dst_dir}/{first_file_name}")
    print(f"Copied {first_file_name}")

    for i in range(1, len(available_dates)):
        prev_dt = available_dates[i-1]
        curr_dt = available_dates[i]
        curr_dt_fmt = ''.join(curr_dt.split('-'))

        curr_file_name = f"CommonCols_County_Data_Community_Profile_Report_{curr_dt_fmt}_Public.xlsx"

        # Copy the currrent file
        shutil.copy(f"{src_dir}/{curr_file_name}", f"{dst_dir}/{curr_file_name}")
        print(f"Copied {curr_file_name}")

        prev_dt_obj = datetime.strptime(prev_dt, '%Y-%m-%d')
        curr_dt_obj = datetime.strptime(curr_dt, '%Y-%m-%d')

        gap = (curr_dt_obj - prev_dt_obj).days

        # Copy any gap files
        if gap > 1:
            org_file_name = f"CommonCols_County_Data_Community_Profile_Report_{curr_dt_fmt}_Public.xlsx"
            for i in range(1, gap):
                new_dt = curr_dt_obj - timedelta(days=i)
                new_dt_iso = new_dt.date().isoformat()
                new_dt_fmt = ''.join(new_dt_iso.split('-'))
                new_file_name = f"CommonCols_County_Data_Community_Profile_Report_{new_dt_fmt}_Public.xlsx"

                shutil.copy(f"{src_dir}/{org_file_name}", f"{dst_dir}/{new_file_name}")
                print(f"Copied {new_file_name}")




