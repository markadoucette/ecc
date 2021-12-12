import pandas as pd
import numpy as np

# Electric Car Data Set
def ev_data(ev_raw):

    # Read in EV data

    # ev_raw = pd.read_csv('./app/data_files/ev_car_final.csv',index_col=0)

    # Set model name to index
    ev_raw.set_index('Model', drop=True, inplace=True)

    # Create series for range
    ev_range = ev_raw["range_raw"]
    # Make copy for display purposes
    ev_df = ev_raw[['Brand', 'Battery Size (kWh)', 'Segment', 'Powertrian',
           'BodyStyle', 'Seats', '0 - 62 MPH (Sec)', 'Top Speed (MPH)',
           'Range (Mi)', 'Efficiency (Wh/mi)', 'Euro',]].copy()

    # mappings for columns
    format_mapping= {
                      'Euro': "€{:,.0f}"
                     }
    # apply mapping to columns
    for key, value in format_mapping.items():
        ev_df[key] = ev_df[key].apply(value.format)

    return ev_raw,ev_range,ev_df

def get_range(ev_range,car_id):
    return ev_range.loc[car_id]


def get_comparison_table(ev_df,car_1,car_2):
    c_table = ev_df.loc[[car_1,car_2]].transpose()
#     f_table['diff'] = (f_table[car_1]-f_table[car_2])
    return c_table
