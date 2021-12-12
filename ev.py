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


def get_corr(ev_raw):
    # Subset columns to one needed for correlation recomendation system
    ev_df = ev_raw.iloc[:,[1,3,4,5,15,16,17,18]]

    # Convert cagetorical columns into numerical and transpose
    ev_df = pd.get_dummies(ev_df,drop_first = True).T

    # Get correlations of vehicles with other vehicles 
    corr = ev_df.corr()

    # Set the diagonal values to nan
    np.fill_diagonal(corr.values, np.nan)

    # Get top 10 vehicles similar to  root vehicle
    top10 = np.argsort(-corr.values, axis=1)[:, :10]

    # Get correlation as numpy array for capturing values
    corr_values = corr.to_numpy()

    # Empty list
    ev_top = []

    # Loop through the top 10 correlations and build data frame

    for i in  range(len(top10)):
            for j in range(len(top10[i])):

                model =  corr.columns[i]
                comparison_model =corr.columns[top10[i][j]]
                correlation = corr_values[i][top10[i][j]]

                ev_top.append([model,comparison_model,correlation])

    corr_final = pd.DataFrame(ev_top, columns=["Model", "Comparison Model","Correlation"])
    
    return corr_final
    
def get_similar(corr_final,car_id):
    similar_df = corr_final.loc[(corr_final['Model']== car_id)][["Comparison Model","Correlation"]]
    return similar_df