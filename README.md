
#### _For [Dr. Umay Suanda's](https://psych.uconn.edu/faculty/umay-suanda/) Communication and Development lab_

## LangMatrix

This program generates a co-occurrence matrix amongst a collection of text files. This co-occurrence matrix compares all the unique words to their frequency across a collection of texts.


### Table of Contents
1. [Preparing Input Data](README.md#preparing-data)
2. [Starting the Analysis](README.md#running-analysis)
3. [Results](README.md#results)
4. [Build Instructions](README.md#build-instructions)


## Preparing Data

To analyze a set of files, create a new `.txt` file that contains a list of all the filenames.

- There are no naming limitations. Keep in mind that the name of **this** input file will be used in naming the output file
- There is no limit to how long the list can be, but be aware that it will take longer to analyze.
- example: the file `pb_listA.txt` contains the following
```
rawtext_drseussabc.csv
rawtext_goodnightmoon.csv
rawtext_greeneggsandham.csv
```

The `files_list.txt` file must be located at the root/parent folder. Otherwise the files on that list cannot be found, and subsequently will not be analyzed.
  - example:
    ```
    Picture Books
    ├─ pb_listA.txt  
    ├─ drseussabc
    |   └── ...
    ├─ goodnightmoon
    |   └──...
    |...
    ```
  - If you'd like to analyze more than one group of files, such as transcripts from two different studies, a second list of files can be added.

## Starting the Analysis

### Steps:

  1. Select the `Upload` button
  2. Next, in the "Analysis Column" indicate where the text column is for that subset of files
     - i.e. column **C** for the Rollins transcripts, in our lab
       - That is the third column with all the transcribed utterances
  3. Repeat 1+2 for a second list of files, if needed
  4. If needed, change the save folder by selecting the `Pick folder` button
  5. Click `Start Analysis` to begin

*This process may take a while, due to project limitations.*

To help, there are a few information boxes that will pop up to inform you of its current progress. They indicate when the program is starting to...
1. Collect the set of files, from the given `file_list.txt`(s)
2. Read through each file and analyze each's unique word frequency
3. The co-occurrence matrix(s) were successfully saved

#### NOTE: *You* **must** *click "ok" for the analysis to continue*.


## Results
All output files go into the results folder, by default.
When the program opens, it creates a new folder in the result folder. For the sake of flexibility and organization, it is named `YYYY-DD-MM`

In the output files there is...

- A co-occurrence matrix file for *each* file list given
  - naming schema: `[filename]_matrix.csv` 
  - i.e. `pb_listA_matrix.csv`
- A master co-occurrence matrix, if given two lists
  - naming schema: `[filenameA]-[filenameB]_master_matrix.csv` 
  - i.e. `pb_listA-6mo_master_matrix.csv`

Each matrix is formatted like the following:
```

    | subject1file | subject2file | subject3file | ...
--------------------------------------------------------
6   |            0 |            0 |            1 | ...
a.m.|           22 |           11 |           25 | ...
able|            4 |            1 |            0 | ...
...
```
In the case of 2 list of files, it is the same format and the header includes *all* the files.
Note that if the analysis is repeated, the old files are NOT overwritten. The newer ones will end in `..._1.csv` or so on.

Example results folder:
```
    ├── Results
        ├── 2020-03-05
        |   └── 9mo_matrix.csv
        |   └── 6mo_matrix.csv
        |   └── 6mo-9mo_master_matrix.csv
        |   └── 6mo_matrix_1.csv
        |   └── pb_listA_matrix.csv
        |   └── 6mo-pb_listA_master_matrix.csv
        ├── 2020-03-26
            └── 9mo_matrix.csv
            └── 9mo_matrix_1.csv
            └── pb_listA_matrix.csv
            └── 9mo-pb_listA_master_matrix.csv
```


### Build Instructions
To run from the source code, `pandas` and `PySide2` are required.
In `langmatrix.py`, the following code has been commented out. However if you're on Windows, re-enabling it causes the custom icon to show up on the taskbar, instead of the Python logo.
```python
import ctypes
...
...
# lines 115-118
    # for Windows
    myappid = u"mycompany.myproduct.subproduct.version"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # from ctypes
    app.setWindowIcon(QtGui.QIcon('resources/main.ico'))
```

The icon was created by [dAKirby309](https://www.deviantart.com/dakirby309)
