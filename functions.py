import math
import csv
import numpy as np
from dicts import trailer_costs, pipeline_costs


def get_distance_from_prod_to_demand_site(prod_site, demand_site, distance_matrix):
    """Locates and returns the distance between the production and demand sites.

    :param prod_site: production site name
    :type prod_site: str
    :param demand_site: demand site name
    :type demand_site: str
    :param distance_matrix: distance matrix dataframe
    :type distance_matrix: dataframe
    :return: distance between the production site and demand site [km]
    """
    distance_between_sites = distance_matrix[prod_site][demand_site]
    return distance_between_sites


def get_annual_h2_production(prod_site, annual_h2_prod_df):
    # ToDo: write test that makes sure only a production site is located
    """Locates and returns the annual H2 production for the production site.

    :param prod_site: production site name
    :type prod_site: str
    :param annual_h2_df: annual H2 production dataframe
    :type annual_h2_prod_df: dataframe
    :return: annual H2 production for production site
    """
    h2_yearly_prod = annual_h2_prod_df.loc[prod_site][0]
    return h2_yearly_prod


def get_annual_h2_demand(demand_site, annual_h2_demand_df):
    # ToDo: write tests that make sure only a demand site is located
    """Locates and returns the annual H2 demand for the production site.

    :param demand_site: demand site name
    :param annual_h2_df: annual H2 demand dataframe
    :return: annual H2 demand for demand site
    """
    h2_yearly_demand = annual_h2_demand_df.loc[demand_site][0]
    return h2_yearly_demand


def get_total_h2_loading(h2_yearly_prod, h2_yearly_demand):
    """Determines what is the amount of H2 that can be transported between the sites.

    :param h2_yearly_prod: yearly H2 production at production site [kgH2]
    :type h2_yearly_prod: number
    :param h2_yearly_demand: yearly H2 demand at demand site [kgH2]
    :type h2_yearly_demand: number
    :return: total H2 loading amount [kgH2]
    """
    total_h2_loading = min(h2_yearly_prod, h2_yearly_demand)
    return total_h2_loading


# ToDo: get_compressor_costs can either be a function or a method of the site classes,
#  def get_compressor_costs(prod_site, demand_site, compressor_costs, transport_pressure):
#       compressor costs are two compressions (at prod site and demand site) so two costs
#       we need the transported amount of H2 so here calculate the loading (call from site objects -> available H2 prod site + available H2 demand site)
#       in trailer transport, the compressor needs to compress to trailer level, at demand site compressor needs to compress H2 to needed pressure
#       if we know transport pressure, we know how much we need to compress for demand site: check the compressor size at production site
#           - > at initialisation, it would be 0. Then we increase compressor sizes
#       call get_compression_costs which is a function of mass flow at production site, and pressure (350 bar) and compressor cost dict -> this is our cost before
#       for cost after, same call as line above, but here we add available H2 -> costs will go lower depending on how big the compressor is
#       same needs to be done at demand site, which takes difference of transport pressure to demand pressure
#       we dont know which trailer/pipeline we are
#       include pressure for each transport type in their dicts and then use as input
#       in get_trailer_costs we call get_compressor_costs and swap transport_pressure for trailer_type['pressure'] from dict


def get_trailer_costs(total_h2_loading, distance, trailer_costs):
    # ToDo: make sure that the costs are calculated properly, check all parameters are relevant,
    #  make sure it should be total_H2_loading / 365 for the mass flow
    #  - got whole calculation from 'lausitz_surface_graph'
    """Calculates the cost per kg to transport the H2 by trailers for each trailer type,
    and adds each cost per kg to a dictionary.

    :param total_h2_loading: total H2 loading amount [kgH2]
    :type total_h2_loading: number
    :param distance: distance between the production site and demand site [km]
    :type distance: number
    :param trailer_costs: dict for trailer cost information for each trailer type
    :type trailer_costs: dict
    :return: trailer cost per kg dict
    """

    cost_per_kg_trailer = {}

    for trailer_type in trailer_costs:
        trailer = trailer_costs[trailer_type]

        trailer_capex = (total_h2_loading / 365 / trailer['trailer_cap']) * \
                        (((distance * 2) / trailer['av_speed']) + trailer['unload_time']) / \
                        (trailer['delivery_days'] * trailer['trailer_availability'] * trailer['driver_hours']) * \
                        (trailer['crf_trailer'] * trailer['tube_trailer_cost'] * trailer['crf_cab'] * trailer['cab_cost'])

        trailer_opex_fix = 0.05 * trailer_capex  # 5 % of CAPEX

        trailer_opex_var = (0.01 * trailer_capex) + \
                           (distance * trailer['maut'] * trailer['maut_distance']) + \
                           (distance * 2 * trailer['fuel_price'] * trailer['fuel_economy']) + \
                           (total_h2_loading / 365 / trailer['trailer_cap']) * \
                           ((distance * 2 / trailer['av_speed']) + trailer['unload_time']) * \
                           (distance * 2 / trailer['av_speed']) * trailer['drivers_wage']

        trailer_cost_tot = trailer_capex + trailer_opex_fix + trailer_opex_var
        if total_h2_loading > 0:
            cost_per_kg_trailer[trailer_type] = trailer_cost_tot / total_h2_loading
        else:
            cost_per_kg_trailer = None
    return cost_per_kg_trailer


def get_pipeline_costs(total_h2_loading, distance, pipeline_costs):
    # ToDo: make sure costs are calculated correctly
    # ToDo: decide if the diameter of the pipeline needs to be considered
    """Calculates the cost per kg to transport the H2 by pipeline for each pipeline type,
    and adds each cost per kg to a dictionary.

    :param total_h2_loading: total H2 loading amount [kgH2]
    :param distance: distance between the production site and demand site [km]
    :param pipeline_costs: dict for pipeline cost information for each pipeline type
    :return: pipeline cost per kg dict
    """

    cost_per_kg_pipeline = {}

    for pipeline_type in pipeline_costs:
        pl = pipeline_costs[pipeline_type]
        pipeline_capex = pl['crf'] * (distance * pl['cost_per_km'])
        pipeline_opex_fix = 0.04 * pipeline_capex
        pipeline_cost_tot = pipeline_capex + pipeline_opex_fix
        if total_h2_loading > 0:
            cost_per_kg_pipeline[pipeline_type] = pipeline_cost_tot / total_h2_loading
        else:
            cost_per_kg_pipeline = None
        return cost_per_kg_pipeline


def get_cheapest_cost(costs_dict_specific, dict_entries):
    """Finds the cheapest cost in the specific costs dictionary, returning a list of the
    production site, demand site, mode of transport and the cheapest specific value (EUR/kg).

    :param costs_dict_specific: specific costs dictionary
    :type: dict
    :param dict_entries: list of the strings of entry names in specific costs dictionary,
    for each production and demand site
    :type: list
    :return: Cheapest specific cost + relevant parameters
    """
    # Creates an empty list in preparation for the information regarding the
    # cheapest transport option e.g.
    # [production site, demand site, transport mode, specific costs [EUR/kg]]
    minimum = [None, None, None, np.inf]
    # Loops through entire specific costs dictionary
    for prod_entry, dem_entry in costs_dict_specific.items():
        for dem_entry, cost_load_entry in dem_entry.items():
            # Takes only the specific costs from the dictionary and loops through all
            cost_entry_dict = dict((k, cost_load_entry[k]) for k in [dict_entries[0]] if k in cost_load_entry)
            for cost_entry, transport_mode_entry in cost_entry_dict.items():
                for transport_mode_entry, cost_value in transport_mode_entry.items():
                    # If the specific cost of the given transport mode for the given prod/demand
                    # site combination is less than infinity or previous specific cost, update the
                    # minimum list with the current specific cost + information
                    if cost_value < minimum[3]:
                        minimum[0] = prod_entry
                        minimum[1] = dem_entry
                        minimum[2] = transport_mode_entry
                        minimum[3] = cost_value

    return minimum


def run_transport_optimization_model(distance_df, annual_h2_prod_df, annual_h2_demand_df):
    """Main function for running the transport optimization model. For all production and demand sites,
     the transport route and mode with the optimal specific costs will be chosen. Once this particular
     route has been chosen with an optimal transport mode, the route will no longer be considered, and
     the optimal specific costs for the remaining routes and transport modes will be found. This will
     be repeated until there is no more demand left to be fulfilled.

    :param distance_df: distance matrix for all production and demand sites
    :type distance_df: dataframe
    :param annual_h2_prod_df: annual H2 production for each production site
    :type annual_h2_prod_df: dataframe
    :param annual_h2_demand_df: annual H2 demand for each demand site
    :type annual_h2_demand_df: dataframe
    :return: results from transport optimization
    """
    # Empty dict in preparation to be updated for each production site/demand site/transport mode
    costs_dict_specific = {}
    # The entry headers in costs_dict_specific: the specific costs for each transport mode
    # and the total possible loading amount of H2
    dict_entries = ['specific costs', 'loading kgH2']
    # List of all the production site names
    prod_site_list = [row for row in annual_h2_prod_df.index]
    # List of all the demand site names
    demand_site_list = [row for row in annual_h2_demand_df.index]
    # Empty list in preparation to include all the production/demand site combinations that
    # have an optimum specific cost and thus should be removed from costs_dict_specific in
    # the next step
    delete_list = []
    # Empty list in preparation for the final optimization results
    optimization_results = []
    # The cumulative total costs for each of the optimal routes
    total_costs = 0
    # The sum of the demands for all demand sites
    demand_sum = annual_h2_demand_df.sum()[0]

    # While loop until there is no demand left to be fulfilled
    while demand_sum > 0:
        for prod_site in prod_site_list:
            costs_dict_specific[prod_site] = {}
            for demand_site in demand_site_list:
                # If the prod/demand site combination has already had the optimal specific cost in it, it
                # does not get included in the costs_dict_specific for the next times, because the
                # maximal possible loading between them should have already been used
                if [prod_site, demand_site] not in delete_list:
                    costs_dict_specific[prod_site][demand_site] = {}
                    # For each production and demand site, the distance is found between them, the
                    # yearly production and demand are found, and the maximum H2 that can be transported
                    # between the two sites is calculated
                    distance = get_distance_from_prod_to_demand_site(prod_site, demand_site, distance_df)
                    # ToDo: cost_per_kg_trailer + cost_per_kg_pipeline calls this,
                    #  they get these as objects
                    h2_yearly_prod = get_annual_h2_production(prod_site, annual_h2_prod_df)
                    h2_yearly_demand = get_annual_h2_demand(demand_site, annual_h2_demand_df)
                    total_h2_loading = get_total_h2_loading(h2_yearly_prod, h2_yearly_demand)
                    # The specific costs for each trailer type in the trailer dict are calculated
                    # ToDo: calculate total_h2_loading in the cost functions, using prod + demand site objects
                    # ToDo: compressor costs need to be inside cost_per_kg_trailer -> a function
                    #  get_compressor_costs is added at the end of get_transport_costs functions
                    cost_per_kg_trailer = get_trailer_costs(total_h2_loading, distance, trailer_costs)
                    # The specific costs for each pipeline type in the pipeline dict are calculated
                    cost_per_kg_pipeline = get_pipeline_costs(total_h2_loading, distance, pipeline_costs)
                    costs_dict_specific[prod_site][demand_site][dict_entries[0]] = {}
                    costs_dict_specific[prod_site][demand_site][dict_entries[1]] = {}
                    # If there is an entry in the cost_per_kg_trailer dict, add it to costs_dict_specific
                    if cost_per_kg_trailer is not None:
                        costs_dict_specific[prod_site][demand_site][dict_entries[0]].update(cost_per_kg_trailer)
                    # If there is an entry in the cost_per_kg_pipeline dict, add it to costs_dict_specific
                    if cost_per_kg_pipeline is not None:
                        costs_dict_specific[prod_site][demand_site][dict_entries[0]].update(cost_per_kg_pipeline)
                    # Add total loading amount to costs_dict_specific
                    costs_dict_specific[prod_site][demand_site][dict_entries[1]] = total_h2_loading
        # Calculates the minimum specific cost for all of the production site/demand site/transportation
        # mode combinations
        minimum = get_cheapest_cost(costs_dict_specific, dict_entries)
        # Retrieves the loading amount for the optimal transport route
        loading = costs_dict_specific[minimum[0]][minimum[1]][dict_entries[1]]
        # Calculates and updates the new available production amount for chosen production site
        # by subtracting the loading amount
        current_prod_val = annual_h2_prod_df.loc[minimum[0], annual_h2_prod_df.columns[0]]
        new_prod_val = current_prod_val - loading
        annual_h2_prod_df.loc[minimum[0], annual_h2_prod_df.columns[0]] = new_prod_val
        # Calculates and updates the new available demand amount for chosen demand site by subtracting
        # the loading amount
        current_demand_val = annual_h2_demand_df.loc[minimum[1], annual_h2_demand_df.columns[0]]
        new_demand_val = current_demand_val - loading
        annual_h2_demand_df.loc[minimum[1], annual_h2_prod_df.columns[0]] = new_demand_val
        # Round specific cost value to 2dp
        specific_cost_value = round(minimum[3], 2)
        # Add costs of optimal transport route to total costs
        total_costs += loading * specific_cost_value
        # Calculates the total number of trailers required to transport
        # the annual loading amount, if the strings 'trailer' or 'truck' are in the name
        if 'trailer' or 'truck' in minimum[2]:
            number_of_trucks = math.ceil(loading / trailer_costs[minimum[2]]['trailer_cap'])
        # A list of the main results parameters to save
        results_data_info = [minimum[0], minimum[1], loading, minimum[2], number_of_trucks, specific_cost_value,
                             loading * specific_cost_value]
        # Adds the results for this iteration to the total optimization results
        optimization_results.append(results_data_info)

        print(
            f'{minimum[0]} transports {loading} kg of H2 annually to {minimum[1]} '
            f'by transport mode {minimum[2]} at a price of {specific_cost_value} EUR/kg.')
        # Adds the production/demand site combination to a list to delete from
        # costs_dict_specific in the next iteration
        delete_entry = [minimum[0], minimum[1]]
        delete_list.append(delete_entry)
        # Updates total demand amount by subtracting loading value
        demand_sum -= loading

    return optimization_results


def save_results_to_csv(optimization_results):
    """Saves the optimization results to a csv file.

    :param optimization_results: results from transport optimization
    :type optimization_results: list
    :return: csv file of optimization results
    """
    results_headers = ['Production site', 'Demand site', 'Annual H2 transported [kg]', 'Transport mode',
                       'Number of trailers required', 'Specific cost [EUR/kg]', 'Total annual cost [EUR]']

    with open('transport_optimization_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(results_headers)
        writer.writerows(optimization_results)
