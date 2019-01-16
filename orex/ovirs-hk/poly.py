def get_polynomial_func(coefficients):
    def polynomial(x):
        return sum(f * (x ** p) for (p,  f) in enumerate(coefficients))
    return polynomial

    
COEFFICIENTS = {
    "fpe_p5v_v":( 0.3557829, 0.002255737),
    "fpe_p5v_i_sense":(0.3368334, 0.002278928),
    "fpe_p3p3v_digital_i_sense":(0, 0.002442),
    "fpe_p3p3v_analog_i_sense":(0, 0.002442),
    "fpe_p3p3v_digital_v":(0, 0.001221),
    "fpe_p3p3v_analog_v":(0, 0.001221),
    "fpe_p12v_v":(0, 0.003663),
    "fpe_p3p3v_vref_v":(0, 0.001221),
    "fpe_p2p5v_v":(0, 0.001221),
    "vref_hfsc_monitor":(0, 0.001221),
    "adc_reserved_0b":( 0, 0.001221),
    "adc_reserved_0c":( 0, 0.001221),
    "adc_reserved_0d":( 0, 0.001221),
    "adc_reserved_0e":( 0, 0.001221),
    "adc_reserved_0f":( 0, 0.001221),
    "cdh_p12v_v":(2.671963, 0.003169921),
    "cdh_agnd_0x11":(0, 0.001221001),
    "cdh_p5v_v":(0.9636597, 0.001143251),
    "cdh_p3p3v_v":(0.671189, 0.000796274),
    "adc_reserved_14":(0.4818298, 0.000571626),
    "cdh_p1p5v_v":(0.4818298, 0.000571626),
    "cdh_fpga_temp":(85.47075, -0.03131524, -3.3776E-05, 6.12E-08, -4.02E-11, 1.17E-14, -1.28E-18),
    "lvps_p5v_converter_temp":(85.47075, -0.03131524, -3.3776E-05, 6.12E-08, -4.02E-11, 1.17E-14, -1.28E-18),
    "lvps_p3p3v_converter_temp":(85.47075, -0.03131524, -3.3776E-05, 6.12E-08, -4.02E-11, 1.17E-14, -1.28E-18),
    "black_body_temp":(85.47075, -0.03131524, -3.3776E-05, 6.12E-08, -4.02E-11, 1.17E-14, -1.28E-18),
    "adc_reserved_1a":(0, 0.001221),
    "filament_temp":(85.47075, -0.03131524, -3.3776E-05, 6.12E-08, -4.02E-11, 1.17E-14, -1.28E-18),
    "fpe_temp":(50.82, 0.01955, -0.0000274),
    "fpe_asic_temp":(-12620, 11.99, -0.002806),
    "adc_reserved_1e":( 0, 0.001221),
    "adc_reserved_1f":( 0, 0.001221),
    "fpa_moly_a_temp":(-205, 0.02771055, 1.82E-07, 1.71E-11),
    "x2nd_stage_a_temp":(-206, 0.0282296, 1.86E-07, 1.74E-11),
    "yolk_a_temp":(-205, 0.02771055, 1.82E-07, 1.71E-11),
    "x1st_stage_a_temp":(-205, 0.02902522, 1.91E-07, 1.79E-11),
    "foot_a_temp":(-205, 0.02902522, 1.91E-07, 1.79E-11),
    "adc_reserved_25":( 0, 0.001221),
    "adc_reserved_26":( 0, 0.001221),
    "adc_reserved_27":( 0, 0.001221),
    "filament_v":(0, 0.001221),
    "filament_i":(0, 0.000488401),
    "blackbody_v":(0, 0.001221001),
    "blackbody_i":(0, 0.00001561),
    "reserved_2c":(0, 0.001221001),
    "reserved_2d":(6.94E-18, 1.56288E-05),
    "virtual_ground_1_v":(0, 0.001221),
    "virtual_ground_2_v":(0, 0.001221)   
}

FUNCS = dict([(x, get_polynomial_func(c)) for (x, c) in COEFFICIENTS.items()])

def apply(key, value):
    return FUNCS[key](value)
