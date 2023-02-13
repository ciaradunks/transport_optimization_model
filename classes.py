class Site:

    def __init__(self, name, location,  init_total_h2_balance, peak_hourly_H2, h2_pressure, h2_pressure_needed):
        self.name = name
        self.location = location
        self.init_total_h2_balance = init_total_h2_balance
        # ToDo: this isn't included yet in the model, but could be in the future
        self.peak_hourly_H2 = peak_hourly_H2
        self.h2_pressure = h2_pressure
        self.h2_pressure_needed = h2_pressure_needed
        self.remaining_h2_balance = init_total_h2_balance
        self.compressor_size = 0

#object = Site(5, 350, 0)

print('done')

