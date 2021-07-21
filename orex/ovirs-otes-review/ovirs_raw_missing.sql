select ed.*, ee.sha256sum, ee.obsdate  from element ed 
    left join element ee 
        on ee.obsstamp between ed.obsstamp - 60 and ed.obsstamp + 60
            and ee.instrument = ed.instrument 
            and ee.component = ed.component 
            and ee.local_id = ed.local_id  
            and ee.proclevel = ed.proclevel
            and ee.loc = 'existing'            
    where ed.instrument = 'ovirs' 
        and ed.loc='delivered' 
        and ed.proclevel = 'raw'
        and ed.component == 'Array_3D'
        and ee.sha256sum is null