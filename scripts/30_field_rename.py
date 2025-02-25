import os
import pandas as pd

r_map = {
'Cases as a percent of national total - last 7 days':       'Cases as a percent of national total daily',
'Cases - last 7 days':                                      'Daily cases last week',
'Cases per 100k - last 7 days':                             'Cases per 100k daily',
'Deaths - last 7 days':                                     'Deaths daily',
'Deaths per 100k - last 7 days':                            'Deaths per 100k daily',
'Cases - % change':                                         'Cases - % change',
'Deaths - % change':                                        'Deaths - % change',
'Cases as a percent of national total - previous 7 days':   'Cases as a percent of national total daily',
'Cases - previous 7 days':                                  'Daily cases previous week',
'Cases per 100k - previous 7 days':                         'Cases per 100k daily',
'Deaths - previous 7 days':                                 'Deaths daily',
'Deaths per 100k - previous 7 days':                        'Deaths per 100k daily',
'Cumulative cases':                                         'Daily cases',
'Cumulative deaths':                                        'Daily deaths',
'Median test latency - last 7 days':                        'Median test latency daily',
'% tests resulted in 3 or fewer days - last 7 days':        '% tests resulted in 3 or fewer days daily',
'Testing latency - absolute change':                        'Testing latency - absolute change',
'% tests resulted in 3 or fewer days - absolute change':    '% tests resulted in 3 or fewer days - absolute change'
}

inp_dir = "StateWise_Temporal_Static_Case_Joined"
out_dir = "StateWise_Temporal_Static_Case_Joined_Renamed"

states = os.listdir(inp_dir)

for idx, state in enumerate(states):
    print(f"Processing: {state}")
    file_name = os.listdir(f"{inp_dir}/{state}")[0]
    df = pd.read_excel(f"{inp_dir}/{state}/{file_name}")
    df = df.rename(columns=r_map)

    out_path = f"{out_dir}/{state}"
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    df.to_excel(f"{out_dir}/{state}/{file_name}", index=False)

    # if idx == 0:
    #     break