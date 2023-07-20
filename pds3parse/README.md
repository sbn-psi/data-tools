# PDS3 Parser

## Overview

Tools for parsing PDS3 labels.

## Prerequisites

* ply

## Tools

### pds3tocsv.py

Extracts a PDS3 file (or files) into a CSV file. The headers are based on the "path" to each keyword. 
For instance, keywords at the top level have a name matching the keyword name, while keywords under the TABLE object
would have a name of "TABLE.keyword_name". Table columns are a little more complicated, and have names 
such as "TABLE.COLUMN.column_name.keyword_name". The fields are unordered.

#### Usage

`pds3tocsv.py [--output-file file] input_labels`

* `--output-file`: The name of the csv file to write to. Defaults to `out.csv`

### extract_column_defs.py

Extracts a table of column definitions from the output of pds3tocsv.py. The information about each column is a record in the
table, so there is one record per column.

#### Usage

`extract_column-defs.py [--input-file file] [--output-file file] [--object-name name] [--columns-name]`

* `--input-file`: The input file. This should be the output of `pds3tocsv.py`. Defaults to `out.csv`.
* `--output-file`: The table of column definitions to write to. Defaults to `columns.csv`.
* `--object-name`: The name of the data object to traverse. Defaults to `TABLE`.
* `--columns-name`: The type of object underneath the data object to traverse. Defaults to `COLUMNS`.

## Other files

### pds3lex.py

Builds the lexer for pds3parse

### pds3tokens.py

Contains the rules for the lexer

### pds3parse.py

Contains the grammar for PDS3