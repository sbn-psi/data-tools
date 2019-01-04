from field import Field

FIELDS = [
    Field("data_type", 1, 2, "UnsignedMSB2"),
    Field("seconds_raw", 3, 4, "UnsignedMSB4"),
    Field("subseconds_raw", 7, 2, "UnsignedMSB2"),    
    Field("mapcam_fwm_temp", 11, 2, "UnsignedMSB2"),
    Field("mapcam_len_temp", 13, 2, "UnsignedMSB2"),
    Field("samcam_fwm_temp", 15, 2, "UnsignedMSB2"),    
    Field("samcam_len_temp", 17, 2, "UnsignedMSB2"),
    Field("polycam_fom_temp", 19, 2, "UnsignedMSB2"),    
    Field("polycam_mirror_2_temp", 21, 2, "UnsignedMSB2"),
    Field("mapcam_roe_temp", 25, 2, "UnsignedMSB2"),
    Field("samcam_fwh_temp", 27, 2, "UnsignedMSB2"),
    Field("samcam_roe_temp", 29, 2, "UnsignedMSB2"),
    Field("mapcam_fwh_temp", 31, 2, "UnsignedMSB2"),
    Field("polycam_roe_temp", 33, 2, "UnsignedMSB2"),
    Field("polycam_foh_temp", 35, 2, "UnsignedMSB2"),
    Field("polycam_mirror_1_temp", 37, 2, "UnsignedMSB2"),
    Field("htr_test_pt", 39, 2, "UnsignedMSB2"),
    Field("htr_brd_temp", 41, 2, "UnsignedMSB2"),
    Field("dpu_brd_temp", 43, 2, "UnsignedMSB2"),
    Field("lvps_brd_temp", 45, 2, "UnsignedMSB2"),
    Field("motor_brd_temp", 47, 2, "UnsignedMSB2"),
    Field("cur_htr", 57, 2, "UnsignedMSB2"),
    Field("cur_motor", 59, 2, "UnsignedMSB2"),
    Field("cur_index", 61, 2, "UnsignedMSB2"),
    Field("cur_lamp", 63, 2, "UnsignedMSB2"),
    Field("volt_mon_sc", 65, 2, "UnsignedMSB2"),
    Field("volt_mon_minus_24", 69, 2, "UnsignedMSB2"),
    Field("volt_mon_minus_12", 71, 2, "UnsignedMSB2"),
    Field("volt_mon_plus_24", 73, 2, "UnsignedMSB2"),
    Field("volt_4_5_therm_mon_1", 75, 2, "UnsignedMSB2"),
    Field("volt_4_5_therm_mon_2", 77, 2, "UnsignedMSB2"),
    Field("volt_mon_plus_12", 79, 2, "UnsignedMSB2"),
    Field("volt_mon_plus_5", 81, 2, "UnsignedMSB2"),
    Field("vref_mon_plus_5", 83, 2, "UnsignedMSB2"),
    Field("ground", 85, 2, "UnsignedMSB2"),
    Field("mapcam_ccd_temp", 51, 2, "UnsignedMSB2"),
    Field("samcam_ccd_temp", 53, 2, "UnsignedMSB2"),
    Field("polycam_ccd_temp", 67, 2, "UnsignedMSB2"),
    
]

RECORD_LENGTH=150

def extract_record(record):
    if (len(record) < RECORD_LENGTH):
        print "undersized record"

    result = {}
    for f in FIELDS:
        result[f.name] = f.extract(record)
    return result