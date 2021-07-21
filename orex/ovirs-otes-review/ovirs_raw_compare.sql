select 
        ed.filepath as "Delivered File", 
        ed.local_id as "Delivered Id",
        ee.filepath as "Existing File", 
        ee.local_id as "Existing Id",
        --ed.sha256sum as "Delivered Checksum", 
        --ee.sha256sum as "Existing Checksum", 
        case when ed.sha256sum = ee.sha256sum then "Match" else "Mismatch" end as "Result"
    from element ed 
    join element ee 
        on ee.obsstamp between ed.obsstamp - 60 and ed.obsstamp + 60
            and ee.instrument = ed.instrument 
            and ee.component = ed.component 
            and ee.local_id = ed.local_id  
            and ee.proclevel = ed.proclevel
    where ed.instrument = 'ovirs' 
        and ed.loc='delivered' 
        and ee.loc = 'existing'
        and ed.component == 'Array_3D'
        and ed.proclevel = 'raw'
;
