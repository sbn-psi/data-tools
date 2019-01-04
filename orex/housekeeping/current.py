GAINS={
    "cur_motor":10.0299,
    "cur_index":24.0,
    "cur_lamp":191.468}
COEFFICIENTS={
    "cur_motor":(-0.37298,1.242960E-01),
    "cur_index":(-0.73974,5.105010E-02),
    "cur_lamp":(-0.290013,6.44952E-03)}

def calc_amperage(vref, gain, h):
    return (vref/gain) * (h/4095.0)

def calc_amperage_ideal(k, h):
    return calc_amperage(5.0, GAINS[k], h) * 1000

def calc_amperage_calibrated(k, h):
    a, b = COEFFICIENTS[k]
    return a + b * h
