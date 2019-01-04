from field import Field

FIELDS = [
    Field("data_type", 1, 2, "UnsignedMSB2"),
    Field("seconds_raw", 3, 4, "UnsignedMSB4"),
    Field("subseconds_raw", 7, 2, "UnsignedMSB2"),    
    Field("mapcam_fwm_temp_x", 11, 4, "SignedMSB4"),
    Field("mapcam_len_temp_x", 15, 4, "SignedMSB4"),
    Field("samcam_fwm_temp_x", 19, 4, "SignedMSB4"),
    Field("samcam_len_temp_x", 23, 4, "SignedMSB4"),
    Field("polycam_fom_temp_x", 27, 4, "SignedMSB4"),    
    Field("polycam_mirror_2_temp_x", 31, 4, "SignedMSB4"),
    Field("mapcam_roe_temp_x", 39, 4, "SignedMSB4"),
    Field("samcam_fwh_temp_x", 43, 4, "SignedMSB4"),
    Field("samcam_roe_temp_x", 47, 4, "SignedMSB4"),
    Field("mapcam_fwh_temp_x", 51, 4, "SignedMSB4"),
    Field("polycam_roe_temp_x",55, 4, "SignedMSB4"),
    Field("polycam_foh_temp_x", 59, 4, "SignedMSB4"),
    Field("polycam_mirror_1_temp_x", 63, 4, "SignedMSB4"),
    Field("htr_brd_temp_x", 71, 4, "SignedMSB4"),
    Field("dpu_brd_temp_x", 75, 4, "SignedMSB4"),
    Field("lvps_brd_temp_x", 79, 4, "SignedMSB4"),
    Field("motor_brd_temp_x", 83, 4, "SignedMSB4"),
    Field("cur_htr_x", 103, 4, "SignedMSB4"),    
    Field("cur_motor_x", 107, 4, "SignedMSB4"),
    Field("cur_index_x", 111, 4, "SignedMSB4"),
    Field("cur_lamp_x", 115, 4, "SignedMSB4"),
    Field("volt_mon_sc_x", 119, 4, "SignedMSB4"),
    Field("htr_test_pt_x", 67, 4, "SignedMSB4"),    
    Field("ground_x", 159, 4, "SignedMSB4"),    
    Field("volt_mon_minus_24_x", 127, 4, "SignedMSB4"),    
    Field("volt_mon_minus_12_x", 131, 4, "SignedMSB4"),    
    Field("volt_mon_plus_24_x", 135, 4, "SignedMSB4"),    
    Field("volt_4_5_therm_mon_1_x", 139, 4, "SignedMSB4"),    
    Field("volt_4_5_therm_mon_2_x", 143, 4, "SignedMSB4"),    
    Field("volt_mon_plus_12_x", 147, 4, "SignedMSB4"),    
    Field("volt_mon_plus_5_x", 151, 4, "SignedMSB4"),    
    Field("vref_mon_plus_5_x", 155, 4, "SignedMSB4"),
    Field("mapcam_ccd_temp_x", 91, 4, "SignedMSB4"),
    Field("samcam_ccd_temp_x", 95, 4, "SignedMSB4"),
    Field("polycam_ccd_temp_x", 123, 4, "SignedMSB4"),    

]

RECORD_LENGTH=226

def extract_record(record):
    result = {}
    for f in FIELDS:
        result[f.name] = f.extract(record)
    return result