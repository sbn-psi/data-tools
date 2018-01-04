import ply.lex as lex
import pds3tokens





lexer = lex.lex(module=pds3tokens)
with open('cdr_f_20050911_20050929.lbl.txt') as f:
  data = f.read()
  lexer.input(data)

while True:
  tok = lexer.token()
  if not tok:
    break
  print(tok)
  
