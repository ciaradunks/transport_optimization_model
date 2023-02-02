# ---------- TRAILER COST DICT ----------
# ToDo: maybe adapt at some point
# ToDo: check all these values or find reference, make sure all are needed
# only different values are trailer capacity and tube trailer cost

trailer_costs = {
    'trailer_300': {
        'trailer_cap': 1165,  # kgH2?
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
        'crf': 0.05,  # 5 %
    },
    'pipeline_retrofit': {
        'cost_per_km': 100000,  # EUR/km
        'crf': 0.05,  # 5 %
    }
}
