import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import arange
#from pylab import meshgrid


def plot_h2_transport_comparison_3d_gas_truck_300(mass_flow, distance):
    # ------------------------ CONSTANTS ------------------------

    crf = 0.07358175
    lcoh_h2_production = 6  # EUR/kg

    # COMPRESSION

    base_capital_cost_compressor_gas_trucks = 28063  # EUR
    scaling_factor_compressor_gas_trucks = 0.6378  # Equation RLI
    crf_compressor_gas_trucks = 0.09  # 15 %
    energy_use_compressor_300_500 = 0.26  # 300 - 500 bar
    energy_use_compressor_20_300 = 1.2  # 20 - 300 bar
    electricity_cost = 0.1855  # EUR/kWh

    # STORAGE GAS
    storage_capacity_gas_trucks = 0.5  # % of daily flow
    storage_cost_gas_trucks = 450  # EUR/kg

    # TRUCKS
    truck_capacity_gas_truck_300 = 1165
    truck_capacity_gas_truck_500 = 1400
    average_speed = 50  # km/h
    unload_time_gas_trucks = 1.5  # h
    crf_trailer_gas_trucks = 0.11  # 11 %
    tube_trailer_cost_gas_truck_300 = 550000  # EUR
    tube_trailer_cost_gas_truck_500 = 1000000  # EUR
    crf_cab_gas_trucks = 0.15  # 15 %
    cab_cost_gas_trucks = 200000
    fuel_price = 1  # EUR/l
    drivers_wage = 35  # EUR/h
    fuel_economy_gas_trucks = 0.3  # l/km
    maut = 0.187  # EUR/km
    maut_distance = 0.8  # %
    delivery_days = 250  # days/year
    truck_availability = 2  # shifts/day
    driver_hours = 4  # hours/shift

    lcoh_gas_trucks_300 = []

    # ------------------------ COMPRESSED GAS TRUCK 300 BAR ------------------------

    # COMPRESSION AT H2 PLANT

    compression_capex_equation_gas_trucks = (base_capital_cost_compressor_gas_trucks *
                                             (mass_flow ** scaling_factor_compressor_gas_trucks))
    compression_capex_gas_trucks = compression_capex_equation_gas_trucks * crf_compressor_gas_trucks
    compression_opex_gas_trucks_fix = 0.04 * compression_capex_equation_gas_trucks
    compression_opex_gas_trucks_var = energy_use_compressor_20_300 * electricity_cost * mass_flow * 365
    compression_costs_tot_gas_trucks = compression_capex_gas_trucks + compression_opex_gas_trucks_fix + \
                                       compression_opex_gas_trucks_var


    # STORAGE AT H2 PLANT
    storage_capex_equation_gas_trucks = storage_capacity_gas_trucks * mass_flow * storage_cost_gas_trucks
    storage_capex_gas_trucks = storage_capex_equation_gas_trucks * crf
    storage_opex_gas_trucks_fix = 0.01 * storage_capex_equation_gas_trucks
    storage_costs_tot_gas_trucks = storage_capex_gas_trucks + storage_opex_gas_trucks_fix

    # TRUCKS
    trucks_capex_300 = (mass_flow / truck_capacity_gas_truck_300) * \
                              (((distance * 2) / average_speed) + unload_time_gas_trucks) / \
                              (delivery_days * truck_availability * driver_hours) * \
                              (crf_trailer_gas_trucks * tube_trailer_cost_gas_truck_300 + crf_cab_gas_trucks *
                               cab_cost_gas_trucks)
    trucks_opex_300_fix = 0.05 * trucks_capex_300  # 5 % of capital
    trucks_opex_300_var = (0.01 * trucks_capex_300) + (distance * maut * maut_distance) + \
                                 (distance * 2 * fuel_price * fuel_economy_gas_trucks) + \
                                 (mass_flow / truck_capacity_gas_truck_300) * \
                                 ((distance * 2 / average_speed) + unload_time_gas_trucks) * \
                                 (distance * 2 / average_speed) * drivers_wage  # 1 % of capital
    trucks_cost_tot_300 = trucks_capex_300 + trucks_opex_300_fix + trucks_opex_300_var

    # COMPRESSION AT DESTINATION

    compression_capex_equation_gas_trucks = (base_capital_cost_compressor_gas_trucks *
                                             (mass_flow ** scaling_factor_compressor_gas_trucks))
    compression_capex_gas_trucks = compression_capex_equation_gas_trucks * crf_compressor_gas_trucks
    compression_opex_gas_trucks_fix = 0.04 * compression_capex_equation_gas_trucks
    compression_opex_gas_trucks_var = energy_use_compressor_300_500 * electricity_cost * mass_flow * 365
    compression_costs_tot_gas_trucks_destination = compression_capex_gas_trucks + compression_opex_gas_trucks_fix + \
                                       compression_opex_gas_trucks_var

    # LEVELIZED COST OF HYDROGEN TRANSPORT
    this_lcoh_gas_trucks_300 = (compression_costs_tot_gas_trucks + storage_costs_tot_gas_trucks +
                                trucks_cost_tot_300 + compression_costs_tot_gas_trucks_destination) / (mass_flow * 365)

    lcoh_gas_trucks_300.append(this_lcoh_gas_trucks_300)

    return this_lcoh_gas_trucks_300

# mass_flow = arange(100, 10000, 100)
# distance = arange(0, 200, 20)
# MF, D = np.meshgrid(mass_flow, distance)
# Z = plot_h2_transport_comparison_3d_gas_truck_300(MF, D)
#
# ax = plt.axes(projection='3d')
# ax.plot_surface(MF, D, Z, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
# ax.set_title('Compressed H2 Gas Trucks')
# ax.set_xlabel('Mass flow (kg/day)')
# ax.set_ylabel('Distance (km)')
# ax.set_zlabel('LCOH (EUR/kg)')
#
# plt.show()
# breakpoint()


def plot_h2_transport_comparison_3d_gas_truck_500(mass_flow, distance):
    # ------------------------ CONSTANTS ------------------------

    crf = 0.07358175
    lcoh_h2_production = 6  # EUR/kg

    # COMPRESSION

    base_capital_cost_compressor_gas_trucks = 28063  # EUR
    scaling_factor_compressor_gas_trucks = 0.6378  # Equation RLI
    crf_compressor_gas_trucks = 0.15  # 15 %
    energy_use_compressor_300 = 1.52  # 300 bar
    energy_use_compressor_500 = 1.86  # 500 bar
    electricity_cost = 0.1855  # EUR/kWh

    # STORAGE GAS
    storage_capacity_gas_trucks = 0.5  # % of daily flow
    storage_cost_gas_trucks = 450  # EUR/kg

    # TRUCKS
    truck_capacity_gas_truck_300 = 1165
    truck_capacity_gas_truck_500 = 1400
    average_speed = 50  # km/h
    unload_time_gas_trucks = 1.5  # h
    crf_trailer_gas_trucks = 0.11  # 11 %
    tube_trailer_cost_gas_truck_300 = 550000  # EUR
    tube_trailer_cost_gas_truck_500 = 1000000  # EUR
    crf_cab_gas_trucks = 0.15  # 15 %
    cab_cost_gas_trucks = 200000
    fuel_price = 1  # EUR/l
    drivers_wage = 35  # EUR/h
    fuel_economy_gas_trucks = 0.3  # l/km
    maut = 0.187  # EUR/km
    maut_distance = 0.8  # %
    delivery_days = 250  # days/year
    truck_availability = 2  # shifts/day
    driver_hours = 4  # hours/shift

    lcoh_gas_trucks_500 = []

    # ------------------------ COMPRESSED GAS TRUCK 500 BAR ------------------------

    # COMPRESSION AT H2 PLANT

    compression_capex_equation_gas_trucks = base_capital_cost_compressor_gas_trucks * \
                                            (mass_flow ** scaling_factor_compressor_gas_trucks)
    compression_capex_gas_trucks = compression_capex_equation_gas_trucks * crf_compressor_gas_trucks
    compression_opex_gas_trucks_fix = 0.04 * compression_capex_equation_gas_trucks
    compression_opex_gas_trucks_var = energy_use_compressor_500 * electricity_cost * mass_flow * 365
    compression_costs_tot_gas_trucks = compression_capex_gas_trucks + compression_opex_gas_trucks_fix + \
                                       compression_opex_gas_trucks_var


    # STORAGE AT H2 PLANT
    storage_capex_equation_gas_trucks = storage_capacity_gas_trucks * mass_flow * storage_cost_gas_trucks
    storage_capex_gas_trucks = storage_capex_equation_gas_trucks * crf
    storage_opex_gas_trucks_fix = 0.01 * storage_capex_equation_gas_trucks
    storage_costs_tot_gas_trucks = storage_capex_gas_trucks + storage_opex_gas_trucks_fix

    # TRUCKS
    trucks_capex_500 = (mass_flow / truck_capacity_gas_truck_500) * \
                              (((distance * 2) / average_speed) + unload_time_gas_trucks) / \
                              (delivery_days * truck_availability * driver_hours) * \
                              (crf_trailer_gas_trucks * tube_trailer_cost_gas_truck_500 +
                               crf_cab_gas_trucks * cab_cost_gas_trucks)
    trucks_opex_500_fix = 0.05 * trucks_capex_500  # 5 % of capital
    trucks_opex_500_var = (0.01 * trucks_capex_500) + \
                                 (distance * maut * maut_distance) + \
                                 (distance * 2 * fuel_price * fuel_economy_gas_trucks) + \
                                 (mass_flow / truck_capacity_gas_truck_500) * \
                                 ((distance * 2 / average_speed) + unload_time_gas_trucks) * \
                                 (distance * 2 / average_speed) * drivers_wage  # 1 % of capital
    trucks_cost_tot_gas_trucks = trucks_capex_500 + trucks_opex_500_fix + trucks_opex_500_var

    # LEVELIZED COST OF HYDROGEN TRANSPORT
    this_lcoh_gas_trucks_500 = (compression_costs_tot_gas_trucks +
                            storage_costs_tot_gas_trucks + trucks_cost_tot_gas_trucks) / (mass_flow * 365)

    lcoh_gas_trucks_500.append(this_lcoh_gas_trucks_500)

    return this_lcoh_gas_trucks_500

# mass_flow = arange(100, 10000, 100)
# distance = arange(0, 200, 20)
# MF, D = np.meshgrid(mass_flow, distance)
# Z = plot_h2_transport_comparison_3d_gas_truck_500(MF, D)
#
# ax = plt.axes(projection='3d')
# ax.plot_surface(MF, D, Z, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
# ax.set_title('Compressed H2 Gas Trucks')
# ax.set_xlabel('Mass flow (kg/day)')
# ax.set_ylabel('Distance (km)')
# ax.set_zlabel('LCOH (EUR/kg)')
#
# plt.show()


def plot_h2_transport_comparison_3d_lohc_truck(mass_flow, distance):
    # ------------------------ CONSTANTS ------------------------

    crf = 0.07358175
    lcoh_h2_production = 6  # EUR/kg
    average_speed = 50  # km/h
    electricity_cost = 0.1855  # EUR/kWh

    # COMPRESSION

    base_capital_cost_compressor_gas_trucks = 28063  # EUR
    scaling_factor_compressor_gas_trucks = 0.6378  # Equation RLI
    crf_compressor_gas_trucks = 0.15  # 15 %
    energy_use_compressor_300 = 1.52  # 300 bar
    energy_use_compressor_300 = 1.86  # 500 bar
    electricity_cost = 0.1855  # EUR/kWh

    # Truck

    truck_capacity_gas_truck_lohc = 1620
    average_speed = 50  # km/h
    unload_time_gas_trucks = 1.5  # h
    crf_trailer_lohc_trucks = 0.11  # 12 %
    tube_trailer_cost_gas_truck_lohc = 150000  # EUR
    crf_cab_gas_trucks = 0.26  # 26 %
    cab_cost_gas_trucks = 200000
    fuel_price = 1  # EUR/l
    drivers_wage = 35  # EUR/h
    fuel_economy_lohc_trucks = 0.3  # l/km
    maut = 0.187  # EUR/km
    maut_distance = 0.8  # %
    delivery_days = 250  # days/year
    truck_availability = 2  # shifts/day
    driver_hours = 4  # hours/shift

    # HYDROGENATION

    # base_capital_cost_hydrogenation_lohc_trucks = 74657 # EUR
    # ref_cap_hydrogenation = 1  # kg/h
    # scaling_factor_lohc_hydrogenation = 0.6
    energy_use_hydrogenation = 0.37  # kWh/kg
    # LOHC_costs = 4  # EUR/kg
    capex_hydro = 1.6 # EUR/kgH2

    # DEHYDROGENATION

    # base_capital_cost_dehydrogenation_lohc_trucks = 55707 # EUR
    # ref_cap_dehydrogenation = 45  # kg/h
    # scaling_factor_lohc_dehydrogenation = 0.6
    capex_dehydro = 5.2 # EUR/kgH2
    energy_use_dehydrogenation = 0.37  # kWh/kg
    heat_demand = 9.1  # kWh/kg
    heat_cost = 0.04  # EUR/kWh
    crf_dehydro = 0.114149039 # 11 years

    # STORAGE LOHC
    storage_capacity_lohc = 0.5  # % of daily flow
    storage_cost_lohc = 50  # EUR/kg

    lcoh_lohc_trucks = []

    # HYDROGENATION AT H2 PLANT

    # hydrogenation_capex_equation = base_capital_cost_hydrogenation_lohc_trucks * \
    #                                ((mass_flow / ref_cap_hydrogenation) ** scaling_factor_lohc_hydrogenation)
    hydrogenation_capex_equation = (7000000 / 1500) * mass_flow
    hydrogenation_capex_lohc_trucks = hydrogenation_capex_equation * crf
    hydrogenation_opex_lohc_trucks_fix = 0.04 * hydrogenation_capex_equation
    hydrogenation_opex_lohc_trucks_var = energy_use_hydrogenation * electricity_cost * mass_flow * 365
    hydrogenation_costs_tot_lohc_trucks = hydrogenation_capex_lohc_trucks + hydrogenation_opex_lohc_trucks_fix \
                                          + hydrogenation_opex_lohc_trucks_var
    # DEHYDROGENATION AT H2 PLANT
    # dehydrogenation_capex_equation = base_capital_cost_dehydrogenation_lohc_trucks * \
    #                                  ((mass_flow / ref_cap_dehydrogenation) ** scaling_factor_lohc_dehydrogenation)
    dehydrogenation_capex_equation = (22000000 / 1500) * mass_flow
    dehydrogenation_capex_lohc_trucks = dehydrogenation_capex_equation * crf_dehydro
    dehydrogenation_opex_lohc_trucks_fix = 0.04 * dehydrogenation_capex_equation
    dehydrogenation_opex_lohc_trucks_var = energy_use_dehydrogenation * electricity_cost * mass_flow * 365 + heat_cost * heat_demand * mass_flow
    dehydrogenation_costs_tot_lohc_trucks = dehydrogenation_capex_lohc_trucks + dehydrogenation_opex_lohc_trucks_fix \
                                            + dehydrogenation_opex_lohc_trucks_var

    # STORAGE AT H2 PLANT
    storage_capex_equation_lohc_trucks = storage_capacity_lohc * mass_flow * storage_cost_lohc
    storage_capex_lohc_trucks = storage_capex_equation_lohc_trucks * crf
    storage_opex_lohc_trucks_fix = 0.01 * storage_capex_equation_lohc_trucks
    storage_costs_tot_lohc_trucks = storage_capex_lohc_trucks + storage_opex_lohc_trucks_fix

    # TRUCKS
    trucks_capex_lohc_trucks = ((mass_flow / truck_capacity_gas_truck_lohc) * \
                               (((distance * 2 / average_speed) + unload_time_gas_trucks) /
                                (delivery_days * truck_availability * driver_hours)) *
                                (crf_trailer_lohc_trucks * tube_trailer_cost_gas_truck_lohc))


    trucks_opex_lohc_trucks_fix = 0.02 * trucks_capex_lohc_trucks
    trucks_opex_lohc_trucks_var = (0.01 * trucks_capex_lohc_trucks) + \
                                  (distance * maut * maut_distance) + \
                                  (distance * 2 * fuel_price * fuel_economy_lohc_trucks) + \
                                  (mass_flow / truck_capacity_gas_truck_lohc) * \
                                  ((distance * 2 / average_speed) + unload_time_gas_trucks) * \
                                  (distance * 2 / average_speed) * drivers_wage  # 1 % of capital

    trucks_cost_tot_lohc_trucks = trucks_capex_lohc_trucks + trucks_opex_lohc_trucks_fix + trucks_opex_lohc_trucks_var

    # # COMPRESSION AT H2 PLANT
    # compression_capex_equation_lohc_trucks = base_capital_cost_compressor_gas_trucks * \
    #                                          (mass_flow ** scaling_factor_compressor_gas_trucks)
    # compression_capex_lohc_trucks = compression_capex_equation_gas_trucks * crf_compressor_gas_trucks
    # compression_opex_lohc_trucks_fix = 0.04 * compression_capex_equation_gas_trucks
    # compression_opex_lohc_trucks_var = energy_use_compressor_300 * electricity_cost * mass_flow * 365
    # compression_costs_tot_gas_trucks =
    # compression_capex_gas_trucks + compression_opex_gas_trucks_fix + compression_opex_gas_trucks_var

    # LEVELIZED COST OF HYDROGEN TRANSPORT
    this_lcoh_lohc_trucks = (hydrogenation_costs_tot_lohc_trucks + storage_costs_tot_lohc_trucks +
                            dehydrogenation_costs_tot_lohc_trucks + trucks_cost_tot_lohc_trucks) / \
                            (mass_flow * 365)

    return this_lcoh_lohc_trucks

# mass_flow = arange(100, 10000, 100)
# distance = arange(0, 200, 20)
# MF, D = np.meshgrid(mass_flow, distance)
# Z = plot_h2_transport_comparison_3d_lohc_truck(MF, D)
#
# ax = plt.axes(projection='3d')
# ax.plot_surface(MF, D, Z, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
# ax.set_title('Lohc H2 Trucks')
# ax.set_xlabel('Mass flow (kg/day)')
# ax.set_ylabel('Distance (km)')
# ax.set_zlabel('LCOH (EUR/kg)')
#
# plt.show()


def plot_h2_transport_comparison_3d_pipeline_100(mass_flow, distance):
    # ------------------------ CONSTANTS ------------------------

    crf = 0.07358175
    lcoh_h2_production = 6  # EUR/kg

    # COMPRESSION

    base_capital_cost_compressor = 28063  # EUR
    scaling_factor_compressor = 0.6378  # Equation RLI
    crf_compressor = 0.15  # 15 %
    energy_use_compressor_20_100 = 0.67  # 20 - 100 bar
    energy_use_compressor_70_500 = 0.94  # 70 - 500 bar

    electricity_cost = 0.1855  # EUR/kWh

    # PIPELINE

    base_capital_cost_compressor_pipeline = base_capital_cost_compressor
    scaling_factor_compressor_pipeline = scaling_factor_compressor
    crf_compressor_pipeline = crf_compressor
    crf_pipeline = 0.05  # 5 %
    pipeline_costs_dn100 = 275500 #365500  # EUR/km

    # ------------------------ PIPELINE ------------------------

    # COMPRESSION AT H2 PLANT

    compression_capex_equation_pipeline = (base_capital_cost_compressor_pipeline *
                                           (mass_flow ** scaling_factor_compressor_pipeline))
    compression_capex_pipeline = compression_capex_equation_pipeline * crf_compressor_pipeline
    compression_opex_pipeline_fix = 0.04 * compression_capex_equation_pipeline
    compression_opex_pipeline_var = energy_use_compressor_20_100 * electricity_cost * mass_flow * 365
    compression_costs_tot_pipeline_plant = compression_capex_pipeline + compression_opex_pipeline_fix \
                                     + compression_opex_pipeline_var

    # PIPELINE DN 100

    pipeline_capital_costs = pipeline_costs_dn100
    pipeline_capex_pipeline = crf_pipeline * (distance * pipeline_capital_costs)
    pipeline_opex_pipeline_fix = 0.04 * pipeline_capex_pipeline  # 4 % of annual costs
    pipeline_cost_tot_pipeline = pipeline_capex_pipeline + pipeline_opex_pipeline_fix

    # COMPRESSION AT DESTINATION
    compression_capex_equation_pipeline = (base_capital_cost_compressor_pipeline *
                                           (mass_flow ** scaling_factor_compressor_pipeline))
    compression_capex_pipeline = compression_capex_equation_pipeline * crf_compressor_pipeline
    compression_opex_pipeline_fix = 0.04 * compression_capex_equation_pipeline
    compression_opex_pipeline_var = energy_use_compressor_70_500 * electricity_cost * mass_flow * 365
    compression_costs_tot_pipeline_destination = compression_capex_pipeline + compression_opex_pipeline_fix \
                                     + compression_opex_pipeline_var


    # LEVELIZED COST OF HYDROGEN TRANSPORT
    this_lcoh_pipeline_100 = (compression_costs_tot_pipeline_plant +  pipeline_cost_tot_pipeline
                              + compression_costs_tot_pipeline_destination) / \
                             (mass_flow * 365)


    return this_lcoh_pipeline_100

# mass_flow = arange(100, 10000, 100)
# distance = arange(0, 200, 20)
# MF, D = np.meshgrid(mass_flow, distance)
# Z = plot_h2_transport_comparison_3d_pipeline_100(MF, D)
#
# ax = plt.axes(projection='3d')
# ax.plot_surface(MF, D, Z, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
# ax.set_title('H2 Pipeline DN 100')
# ax.set_xlabel('Mass flow (kg/day)')
# ax.set_ylabel('Distance (km)')
# ax.set_zlabel('LCOH (EUR/kg)')
#
# plt.show()


def plot_h2_transport_comparison_3d_pipeline_retrofit(mass_flow, distance):
    # ------------------------ CONSTANTS ------------------------

    crf = 0.07358175
    lcoh_h2_production = 6  # EUR/kg

    # COMPRESSION

    base_capital_cost_compressor_gas_trucks = 28063  # EUR
    scaling_factor_compressor_gas_trucks = 0.6378  # Equation RLI
    crf_compressor_gas_trucks = 0.15  # 15 %
    energy_use_compressor_20_100 = 0.67  # 20 - 100 bar
    energy_use_compressor_70_500 = 0.94  # 70 - 500 bar
    energy_use_compressor_20_500 = 1.51  # 70 - 500 bar
    electricity_cost = 0.1855  # EUR/kWh

    # PIPELINE

    base_capital_cost_compressor_pipeline = base_capital_cost_compressor_gas_trucks
    scaling_factor_compressor_pipeline = scaling_factor_compressor_gas_trucks
    crf_compressor_pipeline = crf_compressor_gas_trucks
    crf_pipeline = 0.05  # 5 %
    pipeline_costs_retrofit = 100000 #175000  # EUR/km

    # ------------------------ PIPELINE ------------------------

    # COMPRESSION AT H2 PLANT

    compression_capex_equation_pipeline = (base_capital_cost_compressor_pipeline *
                                           (mass_flow ** scaling_factor_compressor_pipeline))
    compression_capex_pipeline = compression_capex_equation_pipeline * crf_compressor_pipeline
    compression_opex_pipeline_fix = 0.04 * compression_capex_equation_pipeline
    compression_opex_pipeline_var = energy_use_compressor_20_100 * electricity_cost * mass_flow * 365
    compression_costs_tot_pipeline_plant = compression_capex_pipeline + compression_opex_pipeline_fix \
                                           + compression_opex_pipeline_var
    compression_costs_tot_pipeline_plant = 0

    # PIPELINE RETROFIT

    pipeline_capital_costs = pipeline_costs_retrofit
    pipeline_capex_pipeline = crf_pipeline * (distance * pipeline_capital_costs)
    pipeline_opex_pipeline_fix = 0.04 * pipeline_capex_pipeline  # 4 % of annual costs
    pipeline_cost_tot_pipeline = pipeline_capex_pipeline + pipeline_opex_pipeline_fix

    # COMPRESSION AT DESTINATION
    compression_capex_equation_pipeline = (base_capital_cost_compressor_pipeline *
                                           (mass_flow ** scaling_factor_compressor_pipeline))
    compression_capex_pipeline = compression_capex_equation_pipeline * crf_compressor_pipeline
    compression_opex_pipeline_fix = 0.04 * compression_capex_equation_pipeline
    compression_opex_pipeline_var = energy_use_compressor_20_500 * electricity_cost * mass_flow * 365
    compression_costs_tot_pipeline_destination = compression_capex_pipeline + compression_opex_pipeline_fix \
                                                 + compression_opex_pipeline_var

    # LEVELIZED COST OF HYDROGEN TRANSPORT
    this_lcoh_pipeline_retrofit = (compression_costs_tot_pipeline_plant + pipeline_cost_tot_pipeline
                              + compression_costs_tot_pipeline_destination) / \
                             (mass_flow * 365)

    return this_lcoh_pipeline_retrofit


# mass_flow = arange(100, 10000, 100)
# distance = arange(0, 200, 20)
# MF, D = np.meshgrid(mass_flow, distance)
# Z = plot_h2_transport_comparison_3d_pipeline_retrofit(MF, D)
#
# ax = plt.axes(projection='3d')
# ax.plot_surface(MF, D, Z, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
# ax.set_title('H2 Pipeline DN 100')
# ax.set_xlabel('Mass flow (kg/day)')
# ax.set_ylabel('Distance (km)')
# ax.set_zlabel('LCOH (EUR/kg)')
#
# plt.show()


mass_flow = arange(100, 10100, 10)
distance = arange(20, 220, 5)
MF, D = np.meshgrid(mass_flow, distance)
Z_p_retrofit = plot_h2_transport_comparison_3d_pipeline_retrofit(MF, D)
Z_p_100 = plot_h2_transport_comparison_3d_pipeline_100(MF, D)
Z_lohc = plot_h2_transport_comparison_3d_lohc_truck(MF, D)
Z_g_500 = plot_h2_transport_comparison_3d_gas_truck_500(MF, D)
Z_g_300 = plot_h2_transport_comparison_3d_gas_truck_300(MF, D)

t_val = np.zeros((len(distance), len(mass_flow)))
t_type = pd.DataFrame(data= np.zeros((len(distance), len(mass_flow))))
t_t1 = np.empty((len(distance), len(mass_flow)))
t_t2 = np.empty((len(distance), len(mass_flow)))

for ix in range(len(mass_flow)):
    for iy in range(len(distance)):
        v1 = Z_p_retrofit[iy,ix]
        v2 = Z_p_100[iy, ix]
        v3 = Z_lohc[iy, ix]
        v4 = Z_g_500[iy, ix]
        v5 = Z_g_300[iy, ix]
        v = [v1, v2, v3, v4, v5]
        v_min = min(v)
        v_idx = v.index(min(v))
        t_val[iy, ix] = v_min
        if v_idx == 0:
            t_type.iloc[iy, ix] = 'P_R'
            t_t2[iy, ix] = v_min
        if v_idx == 1:
            t_type.iloc[iy, ix] = 'P_N'
        if v_idx == 2:
            t_type.iloc[iy, ix] = 'LOHC'
        if v_idx == 3:
            t_type.iloc[iy, ix] = 'T_500'
            t_t1[iy, ix] = v_min
        if v_idx == 4:
            t_type.iloc[iy, ix] = 'T_300'



np.savetxt("res_g300.csv", Z_g_300, delimiter=",")
np.savetxt("res_g500.csv", Z_g_500, delimiter=",")
np.savetxt("res_lohc.csv", Z_lohc, delimiter=",")
np.savetxt("res_p_r.csv", Z_p_retrofit, delimiter=",")
np.savetxt("res_p_n.csv", Z_p_100, delimiter=",")



ax = plt.axes(projection='3d')
# ax.plot_surface(MF, D, t_val, rstride=1, cstride=1,
#                 cmap='viridis', edgecolor='none')
ax.plot_surface(MF, D, t_t1, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.plot_surface(MF, D, t_t2, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
#ax.set_title('H2 Pipeline DN 100')
ax.set_xlabel('Massenstrom (kg/day)')
ax.set_ylabel('Distanz (km)')
ax.set_zlabel('Transportkosten (EUR/kg)')
ax.set_zlim([0, 3.5])
z_ticks = np.arange(0, 3.5, 0.25)
ax.set_zticks(z_ticks)
x_ticks = np.arange(0, 10000, 1000)
ax.set_xticks(x_ticks)
y_ticks = np.arange(0, 200, 20)
ax.set_yticks(y_ticks)

plt.show()


# plot all separate graphs

ax = plt.axes(projection='3d')
ax.plot_surface(MF, D, Z_p_retrofit, rstride=1, cstride=1,
                edgecolor='none', color='b')
ax.plot_surface(MF, D, Z_p_100 , rstride=1, cstride=1,
                edgecolor='none', color='r')
ax.plot_surface(MF, D, Z_g_300, rstride=1, cstride=1,
                edgecolor='none', color='k')
ax.plot_surface(MF, D, Z_g_500 , rstride=1, cstride=1,
                edgecolor='none', color='y')
ax.plot_surface(MF, D, Z_lohc , rstride=1, cstride=1,
                edgecolor='none', color='g')
#ax.set_title('H2 Pipeline DN 100')
ax.set_xlabel('Masse (kg/day)')
ax.set_ylabel('Distanz (km)')
ax.set_zlabel('Transportkosten (EUR/kg)')
ax.set_zlim([0, 10])
z_ticks = np.arange(0, 10, 0.5)
ax.set_zticks(z_ticks)
x_ticks = np.arange(0, 10000, 1000)
ax.set_xticks(x_ticks)
y_ticks = np.arange(0, 200, 20)
ax.set_yticks(y_ticks)

plt.show()

np.savetxt("res_min.csv", t_val, delimiter=",")
t_type.to_csv('res_type.csv')
