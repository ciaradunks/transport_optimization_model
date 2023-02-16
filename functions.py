import math
import csv
import numpy as np
from dicts import trailer_costs, pipeline_costs, compressor_costs


# ToDo: change a lot of function descriptions and parameters because of new changes

def turn_string_into_value(entry):
    """Removes ' km' from the entry in the dataframe and turns the value into a float, if the value is not 0.

    :param entry: string dataframe entry
    :return: float dataframe entry
    """
    if entry != 0 and ' km' in entry:
        entry = float(entry.replace(' km', ''))
        # ToDo: for some reason this is not working at the moment
        entry = round(entry, 2)
    else:
        entry = entry
    return entry


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
    distance_between_sites = round(distance_matrix[prod_site][demand_site], 2)
    return distance_between_sites


def get_available_h2(prod_site, h2_prod_sites):
    """Locates and returns the annual H2 production for the production site.

    :param prod_site: production site name
    :type prod_site: str
    :param annual_h2_df: annual H2 production dataframe
    :type annual_h2_prod_df: dataframe
    :return: annual H2 production for production site
    """
    h2_available = h2_prod_sites.loc[prod_site]['Available H2']
    return h2_available


def get_needed_h2(demand_site, h2_demand_sites):
    """Locates and returns the annual H2 demand for the production site.

    :param demand_site: demand site name
    :param annual_h2_df: annual H2 demand dataframe
    :return: annual H2 demand for demand site
    """
    h2_needed = h2_demand_sites.loc[demand_site]['H2 needed']
    return h2_needed


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


def get_compressor_costs(total_h2_loading, prod_site, h2_prod_sites, demand_site, h2_demand_sites, cmpr_costs,
                         transport_mode):
    # ToDo: need to figure out if this way actually makes sense, because at the moment
    #  the compressor size for the sites will keep increasing as the function loops through production and
    #  demand sites, meaning the last entry in the dict will surely always have the largest compressor size
    #  so lowest compression costs per kg
    # ToDo: also I have divided the total costs by the compressor size and multiplied by the mass flow
    #  to get the costs for the proportion of the compressor that is used for the specific loading.
    #  Not sure this is the correct way to do it though
    # Gets pressure value for production site (from h2_prod_sites dataframe)
    pressure_1 = h2_prod_sites['H2 pressure'][prod_site]
    # Gets pressure value from transport dict
    pressure_2 = transport_mode['pressure']
    # Gets needed pressure value for demand site (from h2_demand_sites dataframe)
    pressure_3 = h2_demand_sites['H2 pressure needed'][demand_site]
    # checks that the pressure values are not the same and ensures there is a loading amount above zero
    if pressure_1 != pressure_2 and total_h2_loading > 0:
        # new compressor size is calculated as old compressor size + mass flow of this specific compression
        # (average total h2 loading) (kg/day)
        new_cmpr_size = h2_prod_sites['Compressor size'][prod_site] + total_h2_loading / 365
        # equation for investment costs (see lausitz_surface_graph_3d file for the equation)
        eq_prod_site = cmpr_costs['base_capital_cost'] * \
                             ((new_cmpr_size / 365)
                              ** cmpr_costs['scaling_factor'])
        # multiply investment costs by annuity factor
        capex_prod_site = eq_prod_site * cmpr_costs['crf']
        # OPEX is 4 % of investment costs
        opexfix_prod_site = 0.04 * eq_prod_site
        # Gets a string pairing in the form 'x,y' where x is the production site pressure and y is transport pressure
        pressures_prod_site = str(h2_prod_sites['H2 pressure'][prod_site]) + ', ' + \
                              str(transport_mode['pressure'])
        # Calculates variable OPEX for compression (see lausitz file again for equation)
        opexvar_prod_site = cmpr_costs['energy_use'][pressures_prod_site] * \
                            cmpr_costs['elec_price'] * new_cmpr_size
        # Annual production site costs are the investment costs + O&M costs /fixed and variable), then multiplied by
        # the mass flow for this specific compression / the mass flow for the whole compressor, to get the costs
        # only for this specific compression (Note: this might change)
        prod_site_costs = capex_prod_site + opexfix_prod_site + opexvar_prod_site * ((total_h2_loading / 365) / new_cmpr_size)
    else:
        # if the pressures are the same or the loading amount is zero, there is no compression
        prod_site_costs = 0
    # Repeat from comments above for production site compression, just now considering transport and demand site pressures
    if pressure_2 < pressure_3 and total_h2_loading > 0:
        new_cmpr_size = h2_demand_sites['Compressor size'][demand_site] + total_h2_loading / 365
        equation_demand_site = cmpr_costs['base_capital_cost'] * \
                               ((h2_demand_sites['Compressor size'][demand_site] + total_h2_loading / 365)
                                ** cmpr_costs['scaling_factor'])
        capex_demand_site = equation_demand_site * cmpr_costs['crf']
        opexfix_demand_site = 0.04 * equation_demand_site
        pressures_demand_site = str(transport_mode['pressure']) + ', ' + \
                                str(h2_demand_sites['H2 pressure needed'][demand_site])
        opexvar_demand_site = cmpr_costs['energy_use'][pressures_demand_site] * \
                              cmpr_costs['elec_price'] * total_h2_loading
        demand_site_costs = (capex_demand_site + opexfix_demand_site + opexvar_demand_site) * ((total_h2_loading / 365) / new_cmpr_size)
    else:
        demand_site_costs = 0

    cmpr_costs_tot = prod_site_costs + demand_site_costs
    if cmpr_costs_tot != 0:
        cost_per_kg_cmpr = cmpr_costs_tot / total_h2_loading
    else:
        cost_per_kg_cmpr = 0

    return cost_per_kg_cmpr


def get_trailer_costs(total_h2_loading, distance, trailer_costs, compressor_costs,
                      prod_site, h2_prod_sites, demand_site, h2_demand_sites):
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
        if distance > 0:
            trailer_capex = (total_h2_loading / 365 / trailer['trailer_cap']) * \
                            (((distance * 2) / trailer['av_speed']) + trailer['unload_time']) / \
                            (trailer['delivery_days'] * trailer['trailer_availability'] * trailer['driver_hours']) * \
                            (trailer['crf_trailer'] * trailer['tube_trailer_cost'] * trailer['crf_cab'] * trailer[
                                'cab_cost'])

            trailer_opex_fix = 0.05 * trailer_capex  # 5 % of CAPEX
            trailer_opex_var = (0.01 * trailer_capex) + \
                               (distance * trailer['maut'] * trailer['maut_distance']) + \
                               (distance * 2 * trailer['fuel_price'] * trailer['fuel_economy']) + \
                               (total_h2_loading / 365 / trailer['trailer_cap']) * \
                               ((distance * 2 / trailer['av_speed']) + trailer['unload_time']) * \
                               (distance * 2 / trailer['av_speed']) * trailer['drivers_wage']

            trailer_cost_tot = trailer_capex + trailer_opex_fix + trailer_opex_var
        else:
            trailer_cost_tot = 0
        costs_per_kg_compressor = get_compressor_costs(total_h2_loading, prod_site,
                                                       h2_prod_sites, demand_site,
                                                       h2_demand_sites, compressor_costs,
                                                       trailer)
        if total_h2_loading > 0:
            cost_per_kg_trailer[trailer_type] = (trailer_cost_tot / total_h2_loading) + costs_per_kg_compressor
        else:
            cost_per_kg_trailer = None

    return cost_per_kg_trailer


def get_pipeline_costs(total_h2_loading, distance, pipeline_costs, compressor_costs, prod_site, h2_prod_sites,
                       demand_site, h2_demand_sites):
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
        cost_per_kg_compressor = get_compressor_costs(total_h2_loading, prod_site, h2_prod_sites,
                                                demand_site, h2_demand_sites, compressor_costs,
                                                pl)
        if total_h2_loading > 0:
            cost_per_kg_pipeline[pipeline_type] = (pipeline_cost_tot / total_h2_loading) + cost_per_kg_compressor
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


def run_transport_optimization_model(distance_matrix, h2_prod_sites, h2_demand_sites):
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
    prod_site_list = [row for row in h2_prod_sites.index]
    # List of all the demand site names
    demand_site_list = [row for row in h2_demand_sites.index]
    # Empty list in preparation to include all the production/demand site combinations that
    # have an optimum specific cost and thus should be removed from costs_dict_specific in
    # the next step
    delete_list = []
    # Empty list in preparation for the final optimization results
    optimization_results = []
    # The cumulative total costs for each of the optimal routes
    total_costs = 0
    # Add column for the available H2 at the production site, initially this is equal to the total production
    h2_prod_sites['Available H2'] = h2_prod_sites['Total H2 production']
    # Add column for the available H2 at the demand site, initially this is equal to the total demand
    h2_demand_sites['H2 needed'] = h2_demand_sites['Total H2 demand']
    # The sum of the demands for all demand sites
    h2_needed_sum = h2_demand_sites.sum()['H2 needed']
    # Add column for compressor size at production sites (initially this is zero)
    h2_prod_sites['Compressor size'] = 0
    # Add column for compressor size at demand sites (initially this is zero)
    h2_demand_sites['Compressor size'] = 0

    # While loop until there is no demand left to be fulfilled
    while h2_needed_sum > 0:
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
                    distance = get_distance_from_prod_to_demand_site(prod_site, demand_site, distance_matrix)
                    # ToDo: cost_per_kg_trailer + cost_per_kg_pipeline calls this,
                    #  they get these as objects
                    h2_available = get_available_h2(prod_site, h2_prod_sites)
                    h2_needed = get_needed_h2(demand_site, h2_demand_sites)
                    total_h2_loading = get_total_h2_loading(h2_available, h2_needed)
                    # The specific costs for each trailer type in the trailer dict are calculated
                    # ToDo: calculate total_h2_loading in the cost functions, using prod + demand site objects
                    # ToDo: compressor costs need to be inside cost_per_kg_trailer -> a function
                    #  get_compressor_costs is added at the end of get_transport_costs functions
                    cost_per_kg_trailer = get_trailer_costs(total_h2_loading, distance, trailer_costs, compressor_costs,
                                                            prod_site, h2_prod_sites,
                                                            demand_site, h2_demand_sites)
                    # The specific costs for each pipeline type in the pipeline dict are calculated
                    cost_per_kg_pipeline = get_pipeline_costs(total_h2_loading, distance, pipeline_costs,
                                                              compressor_costs, prod_site, h2_prod_sites,
                                                              demand_site, h2_demand_sites)
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
        # Calculates and updates the new available H2 amount for chosen production site
        # by subtracting the loading amount
        current_prod_val = h2_prod_sites.loc[minimum[0], h2_prod_sites.columns[4]]
        new_prod_val = current_prod_val - loading
        h2_prod_sites.loc[minimum[0], h2_prod_sites.columns[4]] = new_prod_val
        # Calculates and updates the new available demand amount for chosen demand site by subtracting
        # the loading amount
        current_demand_val = h2_demand_sites.loc[minimum[1], h2_demand_sites.columns[4]]
        new_demand_val = current_demand_val - loading
        h2_demand_sites.loc[minimum[1], h2_demand_sites.columns[4]] = new_demand_val
        # Round specific cost value to 2dp
        specific_cost_value = round(minimum[3], 2)
        # Add costs of optimal transport route to total costs
        total_costs += loading * specific_cost_value
        # Calculates the total number of trailers required to transport
        # the annual loading amount, if the strings 'trailer' or 'truck' are in the name
        if 'trailer' in minimum[2]:
            number_of_trucks = math.ceil(loading / trailer_costs[minimum[2]]['trailer_cap'])
        else:
            number_of_trucks = 0
        # A list of the main results parameters to save
        results_data_info = [minimum[0], minimum[1], loading, minimum[2], number_of_trucks, specific_cost_value,
                             loading * specific_cost_value]
        # Adds the results for this iteration to the total optimization results
        optimization_results.append(results_data_info)
        # ToDo: what percentage of the production goes to each demand site, also include the distance
        # ToDo:
        print(
            f'{minimum[0]} transports {loading} kg of H2 annually to {minimum[1]} '
            f'by transport mode {minimum[2]} at a price of {specific_cost_value} EUR/kg.')
        # Adds the production/demand site combination to a list to delete from
        # costs_dict_specific in the next iteration
        delete_entry = [minimum[0], minimum[1]]
        delete_list.append(delete_entry)
        # Updates total demand amount by subtracting loading value
        h2_needed_sum -= loading

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
