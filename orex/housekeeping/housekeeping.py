from string import Formatter
import sys
import level0
import level1
import thermistor
import functools
import current
import heater
import voltage_rail
import ccd

THERMISTOR_KEYS=["mapcam_fwm_temp","mapcam_len_temp","samcam_fwm_temp","samcam_len_temp","polycam_fom_temp","polycam_mirror_2_temp","mapcam_roe_temp","samcam_fwh_temp","samcam_roe_temp","mapcam_fwh_temp","polycam_roe_temp","polycam_foh_temp","polycam_mirror_1_temp","htr_brd_temp","motor_brd_temp"]
DPU_THERMISTOR_KEYS=["dpu_brd_temp"]
LVPS_THERMISTOR_KEYS=["lvps_brd_temp"]
VOLTAGE_KEYS=["htr_test_pt","ground","volt_mon_sc","volt_mon_plus_5","volt_mon_plus_12","volt_4_5_therm_mon_1","volt_4_5_therm_mon_2","volt_mon_plus_24","vref_mon_plus_5","volt_mon_minus_12","volt_mon_minus_24"]
CURRENT_KEYS = ["cur_motor","cur_index","cur_lamp"]
CCD_KEYS = ["mapcam_ccd_temp", "samcam_ccd_temp", "polycam_ccd_temp"]


THERMISTOR_FUNCS = {
    "other":functools.partial(thermistor.calibrated_temp, ccm="FM1", thermistor="other"),
    "DPU":functools.partial(thermistor.calibrated_temp, ccm="FM1", thermistor="DPU"),
    "LVPS":functools.partial(thermistor.calibrated_temp, ccm="FM1", thermistor="LVPS")
}


def main(argv):
    if argv is None:
        argv = sys.argv

    l0filename = argv[1]
    l1filename = argv[2]

    records = {}

    for record in extract_records(l0filename, 150):
        extracted = level0.extract_record(record)
        records[timestamp(extracted)] = extracted

    for record in extract_records(l1filename, 226):
        extracted = level1.extract_record(record)
        records[timestamp(extracted)].update(extracted)

    for record in records.values():
        calc_from_dns(record, THERMISTOR_KEYS, thermistor.est_temp, THERMISTOR_FUNCS["other"])
        calc_from_dns(record, DPU_THERMISTOR_KEYS, thermistor.est_temp, THERMISTOR_FUNCS["DPU"])
        calc_from_dns(record, LVPS_THERMISTOR_KEYS, thermistor.est_temp, THERMISTOR_FUNCS["LVPS"])
        calc_keyed(record, CURRENT_KEYS, current.calc_amperage_ideal, current.calc_amperage_calibrated)
        calc_keyed(record, VOLTAGE_KEYS, voltage_rail.voltage_ideal, voltage_rail.voltage_calibrated)

        calc_heater_current(record)
        calc_ccd_temp(record, CCD_KEYS)


    for name in THERMISTOR_KEYS:
        export(records, name, "14.5f")

    for name in DPU_THERMISTOR_KEYS:
        export(records, name, "14.5f")

    for name in LVPS_THERMISTOR_KEYS:
        export(records, name, "14.5f")

    for name in CURRENT_KEYS:
        export(records, name, "14.5f")

    for name in VOLTAGE_KEYS:
        export(records, name, "14.5f")

    for name in CCD_KEYS:
        export(records, name, "14.5f")

    return 0

def extract_records(file, record_length):
    with open(file) as f:
        data = f.read()
        return (data[x:x+record_length] for x in range(0, len(data), record_length))

def timestamp(extracted):
    return extracted["seconds_raw"]*10000 + extracted["subseconds_raw"]

def calc_from_dns(extracted, keys, ideal, calibrated):
    for k in keys:
        dn = extracted[k]
        i = ideal(dn)
        c = calibrated(dn)

        store_values(extracted, k, i, c)

def calc_keyed(extracted, keys, ideal, calibrated):
    for k in keys:
        dn = extracted[k]
        i = ideal(k, dn)
        c = calibrated(k, dn)

        store_values(extracted, k, i, c)

def calc_heater_current(extracted):
    tbrd = extracted["htr_brd_temp_x"]
    tmot = extracted["motor_brd_temp_x"]
    tavg = (tbrd + tmot) / 2.0
    hsc = extracted["volt_mon_sc_x"]
    k = "cur_htr"
    
    dn = extracted[k]

    i = heater.amperage_ideal(dn)
    c = heater.amperage_calibrated(dn, hsc, tavg)

    store_values(extracted, k, i, c)

def calc_ccd_temp(extracted, keys):
    t = extracted["dpu_brd_temp_x"]

    for k in keys:
        dn = extracted[k]

        i = ccd.temp_ideal(k, dn)
        c = ccd.temp_calibrated(k, dn, t)

        store_values(extracted, k, i, c)


def store_values(record, k, i, c):
    kc = k + "_cal"
    ki = k + "_ideal"

    record[kc] = c
    record[ki] = i



def build_format_string(basename, extension_format_spec):
    extensions = ["_x", "_ideal", "_cal"]
    base_format = "{%s}" % basename
    extension_formats = ",".join(["{%s:%s}" % (basename + e, extension_format_spec) for e in extensions])
    return base_format + "," + extension_formats

def field_list(basename):
    extensions = ["", "_x", "_ideal", "_cal"]
    return [basename + x for x in extensions]

def export(records, basename, format_spec):
    do_export(records, basename + ".csv", field_list(basename), build_format_string(basename, format_spec))



def do_export(records, filename, fields, format_str):
    with open(filename, "w") as f:
        f.write(", ".join([k for k in fields]) + "\r\n")
        for r in records.values():
            f.write(Formatter().format(format_str, **r) + "\r\n")


if __name__ == "__main__":
    sys.exit(main(None))