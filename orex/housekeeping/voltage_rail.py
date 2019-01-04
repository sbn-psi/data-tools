COEFFICIENTS = {
    "htr_test_pt":(0,1.221001E-03),
    "ground":(0,1.221001E-03),
    "volt_mon_sc":(0.0242466,8.604870E-03),
    "volt_mon_plus_5":(0,2.442002E-03),
    "volt_mon_plus_12":(0,5.581720E-03),
    "volt_4_5_therm_mon_1":(0,2.930403E-03),
    "volt_4_5_therm_mon_2":(0,2.930403E-03),
    "volt_mon_plus_24":(0,1.343101E-02),
    "vref_mon_plus_5":(0,2.442002E-03),
    "volt_mon_minus_12":(0,-6.802728E-03),
    "volt_mon_minus_24":(0,-1.465201E-02)
}

def voltage_ideal(k, h):
    return 5.0 * (h/4095.0)

def voltage_calibrated(k, h):
    a, b = COEFFICIENTS[k]
    return a + b * h