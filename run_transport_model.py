import numpy as np
import pandas as pd
from functions import run_transport_optimization_model, save_results_to_csv, turn_string_into_value


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


# --------- FUNCTIONS --------- #

import time
t = time.time()

scenario_files = ["Scenario_0_H2_prod.csv",
                  "Scenario_1_H2_prod.csv",
                  "Scenario_2_H2_prod.csv",
                  "Scenario_3_H2_prod.csv",
                  "Scenario_4_H2_prod.csv",
                  "Scenario_5_H2_prod.csv",
                  "Scenario_6_H2_prod.csv"
                  ]

for i, file in enumerate(scenario_files):
    i=5
    h2_prod_sites = pd.read_csv(file, encoding='unicode_escape')
    h2_prod_sites.rename(columns={'Unnamed: 0': 'Production sites'}, inplace=True)
    h2_prod_sites = h2_prod_sites.set_index('Production sites')

    optimization_results = run_transport_optimization_model\
                            (distance_matrix, h2_prod_sites, h2_demand_sites, compressor_cost_flag=False,
                             production_cost_flag=False)
    total_transport_costs=sum([single_transport[-1] for single_transport in optimization_results])
    total_transport_amount = sum([single_transport[2] for single_transport in optimization_results])
    print(f"System {i} leads to an average of {round(total_transport_costs/total_transport_amount,3)} Euro transport costs per kg ")
    save_results_to_csv(optimization_results, suffix="_"+str(i))
