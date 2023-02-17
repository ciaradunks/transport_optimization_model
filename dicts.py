# ---------- TRAILER COST DICT ----------
# ToDo: maybe adapt at some point
# ToDo: check all these values or find reference, make sure all are needed
# only different values are trailer capacity and tube trailer cost

trailer_costs = {
    # ToDo: I have made the trailer 350 bar for now (maybe change back to 300)
    # ToDo: trailer_500 taken out and commented below to test compressor costs (no demand site has 500 bar pressure)
    'trailer_350': {
        'trailer_cap': 1165,  # kgH2?
        'pressure': 350,  # bar
        'tube_trailer_cost': 550000,  # EUR
        'av_speed': 50,  # km/h
        'unload_time': 1.5,  # h
        'crf_trailer': 0.11,  # 11 %
        'crf_cab': 0.15,  # 15 %
        'cab_cost': 200000,  # EUR?
        'fuel_price': 1,  # EUR/l
        'drivers_wage': 35,  # EUR/h
        'fuel_economy': 0.3,  # l/km
        'maut': 0.187,  # EUR/km
        'maut_distance': 0.8,  # %
        'delivery_days': 250,  # days/year
        'trailer_availability': 2,  # shifts/day
        'driver_hours': 4  # hours/shift
    },
    'trailer_500': {
        'trailer_cap': 1400,  # kgH2?
        'pressure': 500,  # bar
        'tube_trailer_cost': 1000000,  # EUR
        'av_speed': 50,  # km/h
        'unload_time': 1.5,  # h
        'crf_trailer': 0.11,  # 11 %
        'crf_cab': 0.15,  # 15 %
        'cab_cost': 200000,  # EUR?
        'fuel_price': 1,  # EUR/l
        'drivers_wage': 35,  # EUR/h
        'fuel_economy': 0.3,  # l/km
        'maut': 0.187,  # EUR/km
        'maut_distance': 0.8,  # %
        'delivery_days': 250,  # days/year
        'trailer_availability': 2,  # shifts/day
        'driver_hours': 4  # hours/shift
    }

}

# ---------- PIPELINE COST DICT ----------
# ToDo: maybe adapt at some point
# ToDo: check all these values or find reference, make sure all are needed
# ToDo: check these are the right pipelines to look at
# so far have only included costs of the pipeline, without compression at H2 plant + destination

pipeline_costs = {
    'pipeline_100': {
        'cost_per_km': 275500,  # EUR/km
        'pressure': 40,
        'crf': 0.05,  # 5 %
    },
    'pipeline_retrofit': {
        'cost_per_km': 100000,  # EUR/km
        'pressure': 40,
        'crf': 0.05,  # 5 %
    }
}

# ---------- COMPRESSOR COST DICT ----------

compressor_costs = {
    'base_capital_cost': 28603,  # EUR
    'scaling_factor': 0.6378,  # Equation (RLI)
    'crf': 0.08,  # 15 %
    'elec_price': 0.1855,  # EUR/kWh
    # ToDo: check where these values come from and which to use
    'energy_use': {
        '40, 350': 1.52,
        '350, 500': 0.26,
        '40, 500': 1.52+0.26,
    }
}

"""
    'trailer_500': {
        'trailer_cap': 1400,  # kgH2?
        'pressure': 500,  # bar
        'tube_trailer_cost': 1000000,  # EUR
        'av_speed': 50,  # km/h
        'unload_time': 1.5,  # h
        'crf_trailer': 0.11,  # 11 %
        'crf_cab': 0.15,  # 15 %
        'cab_cost': 200000,  # EUR?
        'fuel_price': 1,  # EUR/l
        'drivers_wage': 35,  # EUR/h
        'fuel_economy': 0.3,  # l/km
        'maut': 0.187,  # EUR/km
        'maut_distance': 0.8,  # %
        'delivery_days': 250,  # days/year
        'trailer_availability': 2,  # shifts/day
        'driver_hours': 4  # hours/shift
    }
"""