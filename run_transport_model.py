import numpy as np
import pandas as pd
from functions import run_transport_optimization_model, save_results_to_csv, turn_string_into_value
from dicts import compressor_costs, trailer_costs


# --------- INPUTS --------- #

distance_matrix = pd.read_csv('TEST_distance_matrix.csv', encoding='unicode_escape')
distance_matrix.rename(columns={'Unnamed: 0': 'Production/demand sites'}, inplace=True)
distance_matrix = distance_matrix.set_index('Production/demand sites')
distance_matrix = distance_matrix.replace('~', 0, regex=True)
distance_matrix = distance_matrix.apply(np.vectorize(turn_string_into_value))

h2_prod_sites = pd.read_csv('TEST_h2_prod_sites_system1.csv', encoding='unicode_escape')
h2_prod_sites.rename(columns={'Unnamed: 0': 'Production sites'}, inplace=True)
h2_prod_sites = h2_prod_sites.set_index('Production sites')

h2_demand_sites = pd.read_csv('TEST_h2_demand_sites_system1.csv', encoding='unicode_escape')
h2_demand_sites.rename(columns={'Unnamed: 0': 'Demand sites'}, inplace=True)
h2_demand_sites = h2_demand_sites.set_index('Demand sites')

# --------- TESTING --------- #
total_h2_loading = 5000
equation = compressor_costs['base_capital_cost'] * \
           ((total_h2_loading / 365) ** compressor_costs['scaling_factor'])
capex_h2_site = equation * compressor_costs['crf']
opexfix_h2_site = 0.04 * equation
test = str(h2_prod_sites.iloc[0]['H2 pressure']) + ', ' + str(trailer_costs['trailer_350']['pressure'])
opexvar_h2_site = compressor_costs['energy_use'][test] * compressor_costs['elec_price'] * total_h2_loading

# --------- FUNCTIONS --------- #

optimization_results = run_transport_optimization_model(distance_matrix, h2_prod_sites, h2_demand_sites)
save_results_to_csv(optimization_results)
