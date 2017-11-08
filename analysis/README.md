# Analysis

Script to analyze the gcode and to add the metadata to the beginning of the file.

## Installation

```
$ wget https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/master.zip
$ unzip -j master.zip "OctoPrint-MetadataPreprocessor-master/analysis/*" -d analysis
$ cd analysis
$ virtualenv -p /usr/bin/python2 venv
$ ./venv/bin/python setup.py install
```

## Usage

```
$ analysis --help
Usage: analysis [OPTIONS] PATH

Options:
  --speed-x FLOAT
  --speed-y FLOAT
  --speed-z FLOAT
  --offset <FLOAT FLOAT>...
  --max-t INTEGER
  --g90-extruder
  --progress
  --help                     Show this message and exit.
```
