#! /usr/bin/env python3

import ply.yacc as yacc

from pds3tokens import tokens
import pds3lex
import json
import sys
import csv
import itertools
import argparse

def p_label(p):
  'label : statements END'
  p[0] = p[1]
  
def p_statements(p):
  '''statements : statements statement
                | statement'''
  if len(p) > 2:
    p[0] = p[1] + [p[2]]
  else:
    p[0] = [p[1]]
                    
  
def p_statement(p):
  '''statement : attribute_statement
              | pointer_statement
              | object_statement
              | group_statement'''
  p[0] = p[1]
                
def p_assignment_statement(p):
  'attribute_statement : IDENT EQUALS value'
  p[0] = {'type':'attribute', 'name':p[1], 'value':p[3]}
  
def p_pointer_statement(p):
  'pointer_statement : POINTER IDENT EQUALS value'
  p[0] = {'type':'pointer', 'name': '^' + p[2], 'value': p[4]}
  
def p_object_statement(p):
  'object_statement : OBJECT EQUALS IDENT statements END_OBJECT EQUALS IDENT'
  p[0] = {'type':'object', 'name': p[3], 'value': p[4]}
  
def p_group_statement(p):
  'group_statement : GROUP EQUALS IDENT statements END_GROUP EQUALS IDENT'
  p[0] = {'type':'group', 'name': p[3], 'value': p[4]}
  
def p_value(p):
  '''value : scalar_value
           | sequence_value
           | set_value'''
  p[0] = p[1]
           
def p_scalar_value(p):
  '''scalar_value : numeric_value
                  | date_time_val
                  | text_string_value
                  | symbol_value'''
  p[0] = p[1]
                  
def p_numeric_value(p):
  '''numeric_value : INTEGER optional_units_expression
                   | BASED_INT optional_units_expression
                   | REAL optional_units_expression'''
  if (p[2]):
    p[0] = {"scalar": p[1], "unit": p[2] }
  else:
    p[0] = {"scalar": p[1]}
                  
def p_optional_units_expression(p):
  '''optional_units_expression : 
                               | units_expression'''
  if (len(p) > 1):
    p[0] = p[1]
  
def p_units_expression(p):
  '''units_expression : L_ANGLE units_factor R_ANGLE
                      | L_ANGLE units_factor mult_op units_factor R_ANGLE '''
  if (len(p) > 6):
    p[0] = p[2] + p[3] + p[4]
  else:
    p[0] = p[2]
                      
def p_units_factor(p):
  '''units_factor : IDENT 
                  | IDENT EXPONENT INTEGER'''
  if (len(p) > 3):
    p[0] = p[1] + [2] + p[3]
  else:
    p[0] = p[1]
  
def p_mult_op(p):
  '''mult_op : MULTIPLY 
            | DIVIDE'''
  p[0] = p[1]  
  
def p_date_time_val(p):
  '''date_time_val : DATE_TIME_VAL'''
  p[0] = {"scalar": p[1]}
  
  
def p_text_string_value(p):
  '''text_string_value : STRING'''
  p[0] = {"scalar": p[1]}
  
def p_symbol_value(p):
  '''symbol_value : IDENT 
                  | SYMBOL'''
  p[0] = {"scalar": p[1]}
    
def p_sequence_value(p):
  '''sequence_value : sequence_1d 
                  | sequence_2d'''
  p[0] = p[1]
    
def p_sequence_1d(p):
  'sequence_1d : L_PAREN scalar_values R_PAREN'
  p[0] = p[2]
  
def p_scalar_values(p):
  '''scalar_values : scalar_value 
                   | scalar_values SEPARATOR scalar_value'''
  if (len(p) > 3):
    p[0] = p[1] + [p[3]]
  else:
    p[0] = [p[1]]
  
def p_sequence_2d(p):
  'sequence_2d : L_PAREN sequence_1ds R_PAREN'
  
def p_sequence_1ds(p):
  '''sequence_1ds : sequence_1d 
                  | sequence_1ds SEPARATOR sequence_1d'''
  
def p_set_value(p):
  'set_value : L_BRACE scalar_values R_BRACE'
  
def p_error(p):
  print('syntax_error: %s' % p.lineno)
  print(p)
  
parser = yacc.yacc()

def toDict(parsed, context=""):
  result = {}
  for entry in parsed:
    if entry['type'] in ('attribute', 'pointer'):
      values = entry['value']
      if isinstance(values, dict) and 'scalar' in values:
        result[context + entry['name']] = values['scalar'].strip()
      elif isinstance(values, list):
        result[context + entry['name']] = ';'.join([x['scalar'].strip() for x in values])
      else:
        print(entry)
    elif entry['type'] == 'object':
      subresult = toDict(entry['value'], context + entry['name'] + ".")
      result.update(subresult)
    else:
      print(entry)
      
  return result

def main(argv=None):
  argparser = argparse.ArgumentParser()
  argparser.add_argument("labels", nargs="*")
  args = argparser.parse_args()

  if argv is None:
    argv = sys.argv
  
  result = []
  for filepath in args.labels:
    with open(filepath) as f:
      data = f.read()
      parsed = parser.parse(data)
      parsed_dict = toDict(parsed)
      parsed_dict['meta.filepath'] = filepath
      result.append(parsed_dict)
  print(result)
  headers = set(itertools.chain.from_iterable([x.keys() for x in result]))
  with (open('out.csv', 'w')) as outfile:
    csvout = csv.DictWriter(outfile, headers)
    csvout.writeheader()
    csvout.writerows(result)


  
if __name__ == '__main__':
  sys.exit(main())