V2 = 0.201557
VTHERM = 4.54545
R164 = 5000.0
R167 = 49900.0
R173 = 3920.0
A=1.956e-5
B=0.041113

R0CS = {
    "mapcam_ccd_temp": 326.6978205589,
    "samcam_ccd_temp": 331.0751118373,
    "polycam_ccd_temp": 335.3621028386 
}

SLOPES = {
    "mapcam_ccd_temp": 1.3313629162,
    "samcam_ccd_temp": 1.3393694249,
    "polycam_ccd_temp": 1.3549217533 
}

COEFFICIENTS = {
    "mapcam_ccd_temp": (0.186890,-2.701220E-06,8.897210E-05,7.018930E-10),
    "samcam_ccd_temp": (0.186935,-1.541830E-06,8.896410E-05,1.035520E-09),
    "polycam_ccd_temp": (0.186985,-1.978430E-06,8.898940E-05,3.151190E-10)

}

def calc_rccd(hccd):
    return (R164 * (A * hccd + B))/(1 - (A * hccd + B))

def calc_tccd(rccd, r0c, slope):
    return (rccd - r0c)/slope

def temp_ideal(k, h):
    rccd = calc_rccd(h)
    r0c = R0CS[k]
    slope = SLOPES[k]

    return calc_tccd(rccd, r0c, slope)

def temp_calibrated(k, h, t):
    a,b,c,d = COEFFICIENTS[k]
    vi = a + b*t + (c + d * t) * h
    rccd = (R164 * vi)/(VTHERM - vi)

    r0c = R0CS[k]
    slope = SLOPES[k]

    return calc_tccd(rccd, r0c, slope)