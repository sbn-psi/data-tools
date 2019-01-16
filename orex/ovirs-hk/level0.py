from field import Field

FIELDS = [
    Field("idp_ccsds_timestamp", 14, 4, "UnsignedMSB4"),
    Field("fpe_p5v_v", 44, 2, "UnsignedMSB2"),
    Field("fpe_p5v_i_sense", 46, 2, "UnsignedMSB2"),
    Field("fpe_p3p3v_digital_i_sense", 48, 2, "UnsignedMSB2"),
    Field("fpe_p3p3v_analog_i_sense", 50, 2, "UnsignedMSB2"),
    Field("fpe_p3p3v_digital_v", 52, 2, "UnsignedMSB2"),
    Field("fpe_p3p3v_analog_v", 54, 2, "UnsignedMSB2"),
    Field("fpe_p12v_v", 56, 2, "UnsignedMSB2"),
    Field("fpe_n12v_v", 58, 2, "UnsignedMSB2"),
    Field("fpe_p3p3v_vref_v", 60, 2, "UnsignedMSB2"),
    Field("fpe_p2p5v_v", 62, 2, "UnsignedMSB2"),
    Field("vref_hfsc_monitor", 64, 2, "UnsignedMSB2"),
    Field("adc_reserved_0b", 66, 2, "UnsignedMSB2"),
    Field("adc_reserved_0c", 68, 2, "UnsignedMSB2"),
    Field("adc_reserved_0d", 70, 2, "UnsignedMSB2"),
    Field("adc_reserved_0e", 72, 2, "UnsignedMSB2"),
    Field("adc_reserved_0f", 74, 2, "UnsignedMSB2"),
    Field("cdh_p12v_v", 76, 2, "UnsignedMSB2"),
    Field("cdh_agnd_0x11", 78, 2, "UnsignedMSB2"),
    Field("cdh_p5v_v", 80, 2, "UnsignedMSB2"),
    Field("cdh_p3p3v_v", 82, 2, "UnsignedMSB2"),
    Field("adc_reserved_14", 84, 2, "UnsignedMSB2"),
    Field("cdh_p1p5v_v", 86, 2, "UnsignedMSB2"),
    Field("cdh_fpga_temp", 88, 2, "UnsignedMSB2"),
    Field("lvps_p5v_converter_temp", 90, 2, "UnsignedMSB2"),
    Field("lvps_p3p3v_converter_temp", 92, 2, "UnsignedMSB2"),
    Field("black_body_temp", 94, 2, "UnsignedMSB2"),
    Field("adc_reserved_1a", 96, 2, "UnsignedMSB2"),
    Field("filament_temp", 98, 2, "UnsignedMSB2"),
    Field("fpe_temp", 100, 2, "UnsignedMSB2"),
    Field("fpe_asic_temp", 102, 2, "UnsignedMSB2"),
    Field("adc_reserved_1e", 104, 2, "UnsignedMSB2"),
    Field("adc_reserved_1f", 106, 2, "UnsignedMSB2"),
    Field("fpa_moly_a_temp", 108, 2, "UnsignedMSB2"),
    Field("x2nd_stage_a_temp", 110, 2, "UnsignedMSB2"),
    Field("yolk_a_temp", 112, 2, "UnsignedMSB2"),
    Field("x1st_stage_a_temp", 114, 2, "UnsignedMSB2"),
    Field("foot_a_temp", 116, 2, "UnsignedMSB2"),
    Field("adc_reserved_25", 118, 2, "UnsignedMSB2"),
    Field("adc_reserved_26", 120, 2, "UnsignedMSB2"),
    Field("adc_reserved_27", 122, 2, "UnsignedMSB2"),
    Field("filament_v", 124, 2, "UnsignedMSB2"),
    Field("filament_i", 126, 2, "UnsignedMSB2"),
    Field("blackbody_v", 128, 2, "UnsignedMSB2"),
    Field("blackbody_i", 130, 2, "UnsignedMSB2"),
    Field("reserved_2c", 132, 2, "UnsignedMSB2"),
    Field("reserved_2d", 134, 2, "UnsignedMSB2"),
    Field("virtual_ground_1_v", 136, 2, "UnsignedMSB2"),
    Field("virtual_ground_2_v", 138, 2, "UnsignedMSB2")
]

RECORD_LENGTH=221

def extract_record(record):
    result = {}
    for f in FIELDS:
        result[f.name] = f.extract(record)
    return result