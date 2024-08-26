# xed examples

## json Mode

### Replace the old style editor list with a new one

```bash
path/to/xed.py --json rebuild_editor_list.json albedos.xml
```
##  Ad-hoc mode

### replace command: Rename an investigation

```bash
path/to/xed.py --command replace --path "//pds:Investigation_Area/pds:name" --value "No Specific Investigation" albedos.xml
```

### substitute command: Change the collection of the product

```bash
path/to/xed.py --command substitute --path "//pds:Identification_Area/pds:logical_identifier" --search ":data:" --value ":data_derived:" albedos.xml
```


### insert_text command: Add a DOI to the citation information

```bash
path/to/xed.py --command insert_element --path "//pds:Citation_Information" --name "doi" --value "doi placeholder" albedos.xml
```

### insert_text_after command: Add a checksum to the file

```bash
path/to/xed.py --command insert_element_after --path "//pds:File/pds:file_size" --name "md5_checksum" --value "checksum placeholder" albedos.xml
```

### delete command: Remove reference from the reference list

```bash
path/to/xed.py --command delete --path "//pds:Reference_List/pds:External_Reference[pds:reference_text='MORRISON&ZELLNER1979']"  albedos.xml
```

### insert_xml command: Add another modification history

```bash
path/to/xed.py --command insert_xml --path "//pds:Modification_History" --value "<Modification_Detail><modification_date>2024-08-20</modification_date><version_id>1.1</version_id><description>Added another modification history entry</description></Modification_Detail>"  albedos.xml
```

### insert_xml_after command: Add another internal reference

```bash
path/to/xed.py --command insert_xml_after --path "//pds:Reference_List/pds:Internal_Reference[position()=1]" --value "<Internal_Reference><lid_reference>lid placeholder</lid_reference><reference_type>data_to_document</reference_type></Internal_Reference>"  albedos.xml
```

### empty command: Remove all observing system components

**NOTE:** this will leave an empty xml element, which is usually not what you want. This is normally only used to prepare an element for something else.
```bash
path/to/xed.py --command empty --path "//pds:Observing_System" albedos.xml
```