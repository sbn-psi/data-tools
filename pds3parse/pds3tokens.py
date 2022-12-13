#module: pds3tokens.py
import ply.lex as lex
from ply.lex import TOKEN
import re

tokens = (
  'EQUALS',
  'SEPARATOR',
  'MULTIPLY',
  'DIVIDE',
  'L_ANGLE',
  'R_ANGLE',
  'L_PAREN',
  'R_PAREN',
  'L_BRACE',
  'R_BRACE',
  'POINTER',
  'EXPONENT',
  'INTEGER',
  'BASED_INT',
  'REAL',
  'DATE_TIME_VAL',
  'IDENT',
  'STRING',
  'SYMBOL',
  'END',
  'OBJECT',
  'END_OBJECT',
  'GROUP',
  'END_GROUP'
)


t_EQUALS = r'='
t_SEPARATOR = r','
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_L_ANGLE = r'\<'
t_R_ANGLE = r'\>'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_EXPONENT = r'\*\*'
t_POINTER = r'\^'

sign = '[+-]'
unsigned_integer = '\d+'

extended_digit = '[A-Za-z0-9]'
radix = unsigned_integer
based_int = f'{radix}\\#{sign}{extended_digit}\\#'

unscaled_real = f'(({unsigned_integer}\\.({unsigned_integer})?)|(\\.{unsigned_integer}))'
integer = f'{sign}?{unsigned_integer}'
exponent = f'((E{integer})|(e{integer}))'
scaled_real = unscaled_real + exponent
real = f'(({sign}?{scaled_real})|({sign}?{unscaled_real}))'

year = unsigned_integer
month = unsigned_integer
day = unsigned_integer
doy = unsigned_integer

year_doy = f'{year}-{doy}'
year_month_day = f'{year}-{month}-{day}'

date = f'(({year_month_day})|({year_doy}))'

second = f'(({unscaled_real})|({unsigned_integer}))'
minute = unsigned_integer
hour = unsigned_integer
zone_offset = f'{sign}{hour}(:{minute})?'
hour_min_sec = f'{hour}:{minute}(:{second})?'
zoned_time = f'{hour_min_sec}{zone_offset}'
utc_time = f'{hour_min_sec}Z'
local_time = hour_min_sec
time = f'(({utc_time})|({zoned_time})|({local_time}))'

date_time = f'{date}T{time}'
date_time_val = f'(({date_time})|({date})|({time}))'


quoted_text = r'"[^"]*"'

quoted_symbol = r"\'[^']+\'"

letter = '[A-Za-z]'
digit = '[0-9]'
identifier = f'{letter}(({letter})|({digit})|(_{letter})|(_{digit}))*'

t_INTEGER = integer
t_BASED_INT = based_int
t_REAL = real
t_DATE_TIME_VAL = date_time_val

lookup = {'END':'END', 'OBJECT':'OBJECT', 'END_OBJECT':'END_OBJECT', 'GROUP':'GROUP', 'END_GROUP':'END_GROUP'}

@TOKEN(identifier)
def t_IDENT(t):
  t.type = lookup.get(t.value, t.type)
    
  return t

@TOKEN(quoted_text)
def t_STRING(t):
  t.value = re.sub('[" \n]+', ' ', t.value)
  return t
  
t_SYMBOL = quoted_symbol

t_ignore = ' ' 
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  
def t_comment(t):
  r'\/\*.*\*\/'
  

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
