# PDS4 Label Extract

## About

This utility will allow you to query a batch of xml labels for information all at once, and output the results in CSV format, facilitating searches for metadata.

## Usage

`pds4extract.py [--include-filename] [--spec specfile] file(s)`

`--include-filename` will make the name of the label file the first column of the output

`--spec` will will allow you to supply your own csv file containing a list of column names and their associated xpath queries. Without this, only basic information such as LID and start/stop date will be provided.

`file(s)` is the list of label files from which you want to extract information

## About the spec file

The spec file should be a CSV file with two columns: one column will contain the output column name, while the other column will contain the xpath query used to extract the value from the column. See basic.csv for an example.
