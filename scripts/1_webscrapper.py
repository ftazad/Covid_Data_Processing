import requests
from bs4 import BeautifulSoup
from io import StringIO
import json
import pandas as pd

url = "https://healthdata.gov/Health/COVID-19-Community-Profile-Report/gqxm-d9w9/about_data"


response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")


with open("script_tag_20_text.txt", "w", encoding="utf-8") as f:
    for idx, x in enumerate(soup.find_all("script")):
        if idx == 20:
            script_text_1 = str(x)[61:]
            script_text_2 = script_text_1[:752081]
            f.write(script_text_2)


obj = json.load(StringIO(script_text_2))

# file_data_1 = obj['view']['attachments']
file_info = obj['view']['metadata']['attachments']


for idx, file in enumerate(file_info):
    file_name = file['name']
    if file_name.endswith('xlsx'):
        asset_id = file['assetId']
        file_url = f"https://healthdata.gov/api/views/gqxm-d9w9/files/{asset_id}?download=true"
        response = requests.get(file_url)

        if response.status_code == 200:

            # Save the downloaded file in local system
            with open(f"DownloadedFiles/{file_name}", "wb") as file:
                file.write(response.content)
                print(f"File downloaded and saved as: {file_name}")
            
            # Process downloaded file
            df = pd.read_excel(f"DownloadedFiles/{file_name}", sheet_name='Counties', header=1, skiprows=0)
            df.to_excel(f"ProcessedFiles/County_Data_{file_name}", sheet_name='Counties', index=False)
            print(f"  > County data saved as : County_Data_{file_name}")
            
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

