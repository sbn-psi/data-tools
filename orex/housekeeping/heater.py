
R542=1.1
R502=200000
R503=200000
R625=5000
R505 =12.4*1000
R509=6.19*1000
R508=5000
R511=1000

A = 8.37141
B = -3.98570E-02
C = 4.29411E-01
D = -7.67726E-05
E = -2.98350E-03
F = -3.94774E-05

def calc_vhik(ihik):
    return ihik * (R542/4) * ((R625+R503)/R502) * (R505/R509) * (R508/R511)

def calc_ihik(hhik):
    vref = 5.0
    return (vref/2.8233) * (hhik/4095.0)

def amperage_ideal(h):
    return calc_ihik(h) * 1000

def amperage_calibrated(hhtr, hsc, t):
    return A + B * t + (C + D * t) * hhtr + (E + F * t) * hsc