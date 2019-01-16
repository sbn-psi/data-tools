from field import Field

FIELDS = [
    Field("idp_ccsds_timestamp", 6, 4, "UnsignedMSB4"),
    Field("fpe_p5v_v_x", 25, 4, "SignedMSB4"),
    Field("fpe_p5v_i_sense_x", 29, 4, "SignedMSB4"),
    Field("fpe_p3p3v_digital_i_sense_x", 33, 4, "SignedMSB4"),
    Field("fpe_p3p3v_analog_i_sense_x", 37, 4, "SignedMSB4"),
    Field("fpe_p3p3v_digital_v_x", 41, 4, "SignedMSB4"),
    Field("fpe_p3p3v_analog_v_x", 45, 4, "SignedMSB4"),
    Field("fpe_p12v_v_x", 49, 4, "SignedMSB4"),
    Field("fpe_n12v_v_x", 53, 4, "SignedMSB4"),
    Field("fpe_p3p3v_vref_v_x", 57, 4, "SignedMSB4"),
    Field("fpe_p2p5v_v_x", 61, 4, "SignedMSB4"),
    Field("vref_hfsc_monitor_x", 65, 4, "SignedMSB4"),
    Field("adc_reserved_0b_x", 69, 4, "SignedMSB4"),
    Field("adc_reserved_0c_x", 73, 4, "SignedMSB4"),
    Field("adc_reserved_0d_x", 77, 4, "SignedMSB4"),
    Field("adc_reserved_0e_x", 81, 4, "SignedMSB4"),
    Field("adc_reserved_0f_x", 85, 4, "SignedMSB4"),
    Field("cdh_p12v_v_x", 89, 4, "SignedMSB4"),
    Field("cdh_agnd_0x11_x", 93, 4, "SignedMSB4"),
    Field("cdh_p5v_v_x", 97, 4, "SignedMSB4"),
    Field("cdh_p3p3v_v_x", 101, 4, "SignedMSB4"),
    Field("adc_reserved_14_x", 105, 4, "SignedMSB4"),
    Field("cdh_p1p5v_v_x", 109, 4, "SignedMSB4"),
    Field("cdh_fpga_temp_x", 113, 4, "SignedMSB4"),
    Field("lvps_p5v_converter_temp_x", 117, 4, "SignedMSB4"),
    Field("lvps_p3p3v_converter_temp_x", 121, 4, "SignedMSB4"),
    Field("black_body_temp_x", 125, 4, "SignedMSB4"),
    Field("adc_reserved_1a_x", 129, 4, "SignedMSB4"),
    Field("filament_temp_x", 133, 4, "SignedMSB4"),
    Field("fpe_temp_x", 137, 4, "SignedMSB4"),
    Field("fpe_asic_temp_x", 141, 4, "SignedMSB4"),
    Field("adc_reserved_1e_x", 145, 4, "SignedMSB4"),
    Field("adc_reserved_1f_x", 149, 4, "SignedMSB4"),
    Field("fpa_moly_a_temp_x", 153, 4, "SignedMSB4"),
    Field("x2nd_stage_a_temp_x", 157, 4, "SignedMSB4"),
    Field("yolk_a_temp_x", 161, 4, "SignedMSB4"),
    Field("x1st_stage_a_temp_x", 165, 4, "SignedMSB4"),
    Field("foot_a_temp_x", 169, 4, "SignedMSB4"),
    Field("adc_reserved_25_x", 173, 4, "SignedMSB4"),
    Field("adc_reserved_26_x", 177, 4, "SignedMSB4"),
    Field("adc_reserved_27_x", 181, 4, "SignedMSB4"),
    Field("filament_v_x", 185, 4, "SignedMSB4"),
    Field("filament_i_x", 189, 4, "SignedMSB4"),
    Field("blackbody_v_x", 193, 4, "SignedMSB4"),
    Field("blackbody_i_x", 197, 4, "SignedMSB4"),
    Field("reserved_2c_x", 201, 4, "SignedMSB4"),
    Field("reserved_2d_x", 205, 4, "SignedMSB4"),
    Field("virtual_ground_1_v_x", 209, 4, "SignedMSB4"),
    Field("virtual_ground_2_v_x", 213, 4, "SignedMSB4")
]

RECORD_LENGTH=315

def extract_record(record):
    result = {}
    for f in FIELDS:
        result[f.name] = f.extract(record)
    return result