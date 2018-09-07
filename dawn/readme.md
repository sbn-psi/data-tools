# Dawn Data Comparison Tool

This script will compare two dawn data files, and indicate whether or not the files match.

You can run it with the following command:

```
$ dawndiff.py file1 file2
```

## Examples
Files with matching data:

```
$ dawndiff.py V01.IMG V01H.IMG

V01.IMG = V01H.IMG
```


Files with non-matching data:

```
$ dawndiff.py V01.IMG V01H.IMG

V01.IMG != V01X.IMG
```
