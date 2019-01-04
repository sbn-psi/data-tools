import math

VTHERMS = {
    ("FM1", "DPU"):4.54545,
    ("FM1", "LVPS"):4.56000,
    ("FM1", "other"):4.55020,
    ("FM2", "DPU"):4.54545,
    ("FM2", "LVPS"):4.54836,
    ("FM2", "other"):4.54836,
}

VADC_COEFFICIENTS = {
    "FM1":(-4.332800E-04, 1.221460E-03),
    "FM2":(-3.721960E-04, 1.220920E-03)
}

THERMISTOR_COEFFICIENTS = [0.001467062557626247, 0.0002384344349699632, None, 1.007709917088872e-7]

RPULL=5000

# Calibrated version of equation 2
def htherm_to_vadc(a, b, htherm):
    return a + b * htherm


# Calibrated version of equation 4
def vadc_to_rtherm(vadc, vtherm):
    return (RPULL * vadc) / (vtherm - vadc)

def htherm_to_rtherm(htherm, a, b, vtherm):
    vadc = htherm_to_vadc(a, b, htherm)
    return vadc_to_rtherm(vadc, vtherm)

def calibrated_temp(h, ccm, thermistor):
    a,b = VADC_COEFFICIENTS[ccm]
    vtherm = VTHERMS[(ccm, thermistor)]
    rtherm = htherm_to_rtherm(h, a,b, vtherm)
    return ttherm44901(rtherm)

def est_temp(h):
    rtherm = htherm_to_rtherm_ideal(h)
    return ttherm44901(rtherm)

# Equation 5
def htherm_to_rtherm_ideal(htherm):
    return (5000 * htherm) / (3722.7 - htherm)




# wrapper for equation 6 that fills in A0, A1, and A3
def ttherm44901(rthermval):
    a0, a1, _, a3 = THERMISTOR_COEFFICIENTS
    return ttherm(rthermval, a0, a1, a3)

# Equation 6
def ttherm(rthermval, a0, a1, a3):
    if rthermval < 0:
        return -9999999.99999
    ln = math.log(rthermval)
    return 1 / (a0 + (a1 * ln) + (a3 * (ln ** 3))) - 273.15

if __name__ == '__main__':
    rthermval = htherm_to_rtherm_ideal(3191)
    print(rthermval)
    print(ttherm44901(rthermval))

#
#rtherm:6114.5279751597301009
#ln(rtherm):8.718422853835203
#ln(rtherm)^3:662.695142053388247