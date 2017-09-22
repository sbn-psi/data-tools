import sys
import string

NUM_MISSING = '0'
ALPHA_MISSING = '-'

OUTPUT_TEMPLATES = {
    'lc_binary.tab':'{number:>7s} {name:<17s} {designation:<10s} {ref_id:30} {binary_type:1} {binary_type_flag:1} {period:15} {amp1:4} {period2:13} {amp2:4} {p_orb:13} {ds_dp:4} {a_dp:6}',
    'lc_details.tab':'{number:>7s} {name:<17s} {designation:<10s} {h_band:2} {h:5} {h_err:4} {g:6} {g_err:5} {diameter:8} {dia_err:7} {albedo:6}' +
        ' {albedo_err:6} {pflag:1} {pnote:15} {period:15} {period_err:13} {amp_flag:1} {amp_min:4} {amp_max:4} {amp_err:4} {lc_qual:2} {lc_notes:5}' +
        ' {pole:1} {bin_flag:1} {sparse_data:1} {wide_field:1} {ref_id:30}',
    'lc_npa.tab':'{number:>7s} {name:<17s} {designation:<10s} {reference:22s} {par:2s} {period:15s} {amp_max:4s} {period2:13s} {amp2npa:5s}',
    'lc_spinaxis.tab':'{number:>7s} {name:<17s} {designation:<10s} {reference:26} {quality:2} {period:15} {amp_max:4}  {l1:5} {b1:5} {l2:5} {b2:5} {l3:5} {b3:5} {l4:5} {b4:5} {sid_period:13} {shape_model:1}',
    'lc_summary.tab':'{number:>7s} {name:<17s} {designation:<10s} {h:5} {g:6} {diameter:8} {albedo:6} {pflag:1} {pnote:15} {period:15} {amp_flag:1} {amp_min:4} {amp_max:4} {lc_qual:2} {lc_notes:5} {pole:1} {bin_flag:1} {sparse_data:1} {wide_field:1}'
}

MISSING_CONSTANTS = {
    'a_dp': '-9.999',
    'albedo_err': '-.9999',
    'albedo': '-.9999',
    'alternate': '-',
    'amp_err': '-.99',
    'amp_flag': '-',
    'amp_max': '-.99',
    'amp_min': '-.99',
    'amp1': ' -.99',
    'amp2': ' -.99',
    'amp2npa': ' -.99',
    'b1': '-99.9',
    'b2': '-99.9',
    'b3': '-99.9',
    'b4': '-99.9',
    'bin_flag': '.',
    'binary_type_flag': '-',
    'binary_type': '-',
    'designation': '-',
    'dia_error': '-999.999',
    'dia_err': '-99.999',
    'diameter': '-999.999',
    'ds_dp': '-.99',
    'g_err': '-.999',
    'g': '-9.999',
    'h_band': '-',
    'h_err': '-.99',
    'h': '-9.99',
    'l1': '-99.9',
    'l2': '-99.9',
    'l3': '-99.9',
    'l4': '-99.9',
    'lc_notes': '.',
    'lc_qual': '.',
    'name': '-',
    'name': '-',
    'number': '0',
    'p_orb': '-999.99999999',
    'par': '-',
    'period_err': '-999.99999999',	
    'period': '-99999.99999999',
    'period2': '-999.99999999',
    'pflag': '-',
    'pnote': '-',
    'pole': '-',
    'quality': '-',
    'ref_id': '-',
    'shape_model': '-',
    'sid_period': '-999.99999999',
    'sparse_data': '-',
    'wide_field': '-'
}




FIELD_DEFS = {
    'lc_binary.tab': {
        'number': (1,7),
        'name': (9,38),
        'designation':(40,49),
        'ref_id': (51,80),
        'binary_type': (82, 82),
        'binary_type_flag': (83, 83),        
        'period': (85, 97),
        'amp1': (99, 102),
        'period2': (104, 116),
        'amp2': (118, 121),
        'p_orb': (123, 135),
        'ds_dp': (137, 140),
        'a_dp': (142, 147)

    },
    'lc_details.tab': {
        'number':(1,7),
        'name':(9,28),
        'designation': (30,39),
        'h_band':(41,42),
        'h':(44,48),
        'h_err':(50,53),
        'g':(55,60),
        'g_err':(62,66),
        'diameter':(68,75),
        'dia_err':(77,83),
        'albedo':(85,90),
        'albedo_err': (92,97),
        'pflag': (99,99),
        'pnote': (101,115),
        'period': (117,129),
        'period_err': (131,141),
        'amp_flag': (143,143),
        'amp_min': (145,148),
        'amp_max': (150,153),
        'amp_err': (155,158),
        'lc_qual': (160,161),
        'lc_notes': (163,167),
        'pole':(169,169),
        'bin_flag': (171,171),
        'sparse_data':(173,173),
        'wide_field':(175,175),
        'ref_id': (177,206)
    },
    'lc_npa.tab': {
        'number': (1,7),
        'name':(9,38),
        'designation':(40,49),
        'reference':(51,80),
        'par':(82,83),
        'period':(86,97),
        'amp_max':(99,102),
        'period2':(104,116),
        'amp2npa':(118,121)
    },
    'lc_spinaxis.tab': {
        'number':(1,7),
        'name':(9,38),
        'designation':(40,51),
        'reference':(53,82),
        'quality':(84,85),
        'period':(87, 99),
        'amp_max':(101, 104),
        'l1':(106, 110),
        'b1':(112, 116),
        'l2':(118, 122),
        'b2':(124, 128),
        'l3':(130, 134),
        'b3':(136, 140),
        'l4':(142, 146),
        'b4':(148, 152),
        'sid_period':(155, 166),
        'shape_model':(168, 168)
    },
    'lc_summary.tab': {
        'number':(1,7),
        'name':(9,28),
        'designation':(30,39),
        'h':(41,45),
        'g':(47,52),
        'diameter':(54,61),
        'albedo': (63,68),
        'pflag':(70,70),
        'pnote': (72,86),
        'period': (88,100),
        'amp_flag': (102,102),
        'amp_min': (104,107),
        'amp_max': (109,112),
        'lc_qual': (114,115),
        'lc_notes': (117,121),
        'pole': (123,123),
        'bin_flag': (125,125),
        'sparse_data': (127,127),
        'wide_field': (129,129),
    }
}



'''
determines if the specified field overflows its maximum value. This method
works for the object period by default, but can be used for other fields.
'''
def field_overflow(fields, fieldname='period', threshold=9999):
    period = float(fields[fieldname].strip() or '0')
    return period > threshold

'''
determines if the name and provisional id are the same. removes the name
field if they are.
'''
def fix_name(fields):
    if (fields['name'].strip()) == (fields['designation'].strip()):
        fields['name'] = '-'

'''
nudges some fields to the left to compensate for overflows in the period field
'''
def fix_other2(fields):
    if field_overflow(fields):
        fields['other2'] = fields['other2'][1:]

'''
nudges some fields to the left to compensate for overflows in the period field
'''
def fix_binflag(fields):
    if field_overflow(fields):
        fields['bin_flag'] = fields['bin_flag'][1:]

'''
nudges some fields to the left to compensate for overflows in the period field
'''
def fix_period_err(fields):
    if field_overflow(fields):
        fields['period_err'] = fields['period_err'][1:]


'''
period fields that don't overflow have to be nudged to the right to line up with
the fields that do
'''
def fix_period(fields):
    if fields['period']:
        if not field_overflow(fields):
            fields['period'] = ' ' + fields['period']


'''
period3 needs to be nudged to the left if period overflows.
THEN, period3 needs to be nudged to the right if it itself overflows. 
'''
def fix_period3(fields):
    if field_overflow(fields):
        fields['period3'] = fields['period3'][1:]
    if not field_overflow(fields, 'period3'):
        fields['period3'] = ' ' + fields['period3']
        
'''
amp2 fields that don't overflow have to be nudged to the right to line up with
the fields that do
'''
def fix_amp2(fields):
    if not field_overflow(fields, 'amp2npa', 9):
        fields['amp2npa'] = ' ' + fields['amp2npa']
        
'''
garbage values for amp_max should be removed
'''
def fix_amp_max(fields):
    if 'low' in fields['amp_max']:
        fields['amp_max'] = ''

'''
alternate ids (for satellites) need to be normalized to the proper satellide id,
which is (first letter of planet name) + (satellite number)
'''
def fix_alternate(fields):
    if fields['alternate']:
        planet, num = fields['alternate'].split()
        fields['alternate'] = planet[0] + num
        
        
def is_dermawan(fields):
    return fields['number'] == '0' and 'Derm' in fields['name']

def is_comet(fields):
    return 'P/' in fields['name'] or 'P/' in fields['designation']
        

def is_filterable(fields):
    return is_dermawan(fields) or is_comet(fields)

'''
provisional designations for satellites actually need to go into the alternate
id field.
'''
def insert_alternate(fields):
    if fields['designation'] == 'Jupiter VI':
        fields['alternate'] = fields['designation']
        fields['designation'] = ''
    else:
        fields['alternate'] = ''

OLD_FIELD_FUNCTIONS = {
    'name':fix_name,
    'other2':fix_other2,
    'period': fix_period,
    'period3': fix_period3,
    'period_err': fix_period_err,
    'amp2': fix_amp2,
    'amp_max': fix_amp_max,
    'bin_flag': fix_binflag,
    'alternate': fix_alternate
}

FIELD_FUNCTIONS = {
    'name':fix_name,
    'alternate': fix_alternate,
    'amp2npa': fix_amp2
}

UNCERTAINTY_FIELDS = {
    'lc_details.tab' : [('h_err','    '), ('g_err','     ')]
}

NUDGES = {
    'period': 6,
    'period_err': 4
}

def nudge(fields, fieldname, decimal_loc):
    val = fields[fieldname]
    for i in range(0, min(len(val), decimal_loc)):
        if val[i] == '.':
            fields[fieldname] = (' ' * (decimal_loc - i)) + val

def add_missing_constant(fields, fieldname):
    if fieldname in MISSING_CONSTANTS:
        if fields[fieldname].isspace():
            fields[fieldname] = MISSING_CONSTANTS[fieldname]
        else:
            fields[fieldname] = fields[fieldname] or MISSING_CONSTANTS[fieldname]

def remove_negative_uncertainty(line, start, end, replacement):
    val = line[start-1:end+1].strip()
    if val.startswith('-'):
        line = line[:start-1] + replacement + line[end+1:]
    return line



class Rearranger:
    def __init__(self, filename):
        self.filename = filename
        self.field_defs = FIELD_DEFS[filename]
        self.output_format = OUTPUT_TEMPLATES[filename]

    '''
        Process each line in the file
    '''
    def process_file(self):
        return [self.process_line(line_num, self.normalize_line(line)) for
                    line_num, line in enumerate(open(self.filename))]


    '''
        Get the ids, then fix the fields
    '''
    def process_line(self, line_num, line):
        line = self.preprocess_line(line)
    
        fields = self.extract_ids(line)
        
        if is_filterable(fields):
            print 'Notify Carol that she needs to filter: ' + fields['number'] + ' ' + fields['name'] + ' ' + fields['designation']
        
        
        self.fix_fields(fields)
        return self.write_line(fields)
        
    def preprocess_line(self, line):
        line = str.join('', [x for x in line if x in string.printable])
        for fieldname, replacement in UNCERTAINTY_FIELDS.get(self.filename, []):
            start, end = self.field_defs[fieldname]
            line = remove_negative_uncertainty(line, start, end, replacement)
        return line
        
        
    '''
    Pads the output line to a consistent length with spaces
    '''
    def normalize_line(self , line):
    	end_positions = [end for (start, end) in self.field_defs.values()]
    	line_length = max(end_positions)
    	return line.strip('\r\n').ljust(line_length)
        


    '''
    '''
    def extract_ids(self, line):
        values = [(v,line[start-1:end].rstrip()) for 
            (v, (start, end)) in self.field_defs.items()]
        return dict(values)

    '''
    '''
    def fix_fields(self, fields):
        insert_alternate(fields)
        for key in fields.keys():
            if key in FIELD_FUNCTIONS:
                FIELD_FUNCTIONS[key](fields)
            if key in NUDGES:
                nudge(fields, key, NUDGES[key])
            add_missing_constant(fields, key)

    def write_line(self, fields):
        return self.output_format.format(**fields)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    filename = argv[1]
    rearranger = Rearranger(filename)
    lines = [x for x in rearranger.process_file() if x]
    
    outfilename = filename.lower().replace('.tab', '.out.tab')
    open(outfilename, 'w').write('\r\n'.join(lines) + '\r\n')


if __name__ == "__main__":
    sys.exit(main())