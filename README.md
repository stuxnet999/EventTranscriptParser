![logo](./img/logo.png)

### About

**EventTranscriptParser** is python based tool to extract forensically useful details from EventTranscript.db (Windows Diagnostic Database).

The database is found in Windows 10 systems and present at `C:\ProgramData\Microsoft\Diagnosis\EventTranscript\EventTranscript.db`.

The tool currently supports the following features.

+ Extracts Microsoft Edge browsing history
+ Extracts application inventory
+ Extracts Wireless scan results.
+ Extracts successful WiFi connection events
+ Extracts User's default preferences (Video player, default browser etc...)
+ Extracts SRUM information
    + Application execution
    + Application network usage
+ Extracts Application execution activity

### Requirements

Python 3.8 or above. The older versions of Python 3.x should work fine as well.

#### Dependencies

These are the required python libraries/modules needed to run the script

+ json
+ os
+ sqlalchemy
+ csv
+ argparse

All the above modules are available by default in python3. Incase one or the other is missing, you can install by

```
pip install <package-name>
```

### Usage

**Tip**: Before running the tool against the database, make sure that the **-wal (Write Ahead Log)** file data is merged with the original database. Because you might miss out on crucial/juicy data.

The tool is completely CLI based and there are 2 ways to use it.

#### Using Python

```python
python3 EventTranscriptParser.py -f <Path-To-EventTranscript.db> -o <Path-To-Output-Directory>
```
![usage](./img/usage.png)


To view help,
```
python3 EventTranscriptParser.py -h
```

![help](./img/help.png)

#### Using Executable

If you do not have python pre-installed in you system or have issues with the running the script, you can use the compiled executable. The executable is also CLI based.

Download the executable from https://github.com/stuxnet999/EventTranscriptParser/releases

```sh
.\EventTranscriptParser.exe -f .\EventTranscript.db -o .\CSV-Output\
```

The executable was compiled using `pyinstaller`.

#### Compiling on your own

If you wish to compile on your own, use the commands below in any command prompt/terminal window.

```sh
pip install pyinstaller
pyinstaller --onefile EventTranscriptParser.py
```

You will find the compiled executable in the `dist` directory.

### Acknowledgements

This tool wouldn't have been possible without the excellent research & hard work put in by my colleagues [Andrew Rathbun](https://twitter.com/bunsofwrath12) & [Josh Mitchell](https://www.linkedin.com/in/josh-mitchell-0990ba6a/) in investigating the Windows Diagnostic Data.

Read more about their research here - https://github.com/rathbuna/EventTranscript.db-Research

Follow the investigative series at Kroll on EventTranscript.db - https://www.kroll.com/en/insights/publications/cyber/forensically-unpacking-eventtranscript

### Author

Abhiram Kumar

+ Twitter: [@_abhiramkumar](https://www.twitter.com/_abhiramkumar)
+ Personal blog: https://stuxnet999.github.io