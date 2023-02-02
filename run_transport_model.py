import numpy as np
import pandas as pd
from functions import run_transport_optimization_model, save_results_to_csv


# --------- INPUTS --------- #

headers = ['Production site A', 'Production site B', 'Demand site A', 'Demand site B', 'Demand site C']
headers_prod = ['Production site A', 'Production site B']
headers_dem = ['Demand site A', 'Demand site B', 'Demand site C']
annual_production_title = 'Annual H2 production [kg]'
annual_demand_title = 'Annual H2 demand [kg]'

distance_data = [[0, 12, 14, 5, 10], [12, 0, 5, 47, 1], [14, 5, 0, 70, 33], [5, 47, 70, 0, 2], [10, 1, 33, 2, 0]]
annual_h2_prod_data = [100, 90]
annual_h2_demand_data = [30, 90, 50]

distance_array = np.array(distance_data)

distance_df = pd.DataFrame(distance_array, columns=headers, index=headers)
annual_h2_prod_df = pd.DataFrame(annual_h2_prod_data, columns= [annual_production_title], index=headers_prod)
annual_h2_demand_df = pd.DataFrame(annual_h2_demand_data, columns= [annual_demand_title], index=headers_dem)


# --------- FUNCTIONS --------- #

optimization_results = run_transport_optimization_model(distance_df, annual_h2_prod_df, annual_h2_demand_df)
save_results_to_csv(optimization_results)
