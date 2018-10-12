# Dawn Data Comparison Tool

This script will compare two dawn data files, and indicate whether or not the files match.

You can run it with the following command:

```
$ dawndiff.py file1 file2
```

If you want to compare entire directories, use dawndirdiff.py:

```
$ dawndirdiff.py dir1 dir2
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

Directories with matching data:

```
$ ./dawndirdiff.py original similar/

original/V01.IMG = similar/V01.IMG
```

Directories with non-matching data:

```
$ ./dawndirdiff.py original different

original/V01.IMG != different/V01.IMG
```
