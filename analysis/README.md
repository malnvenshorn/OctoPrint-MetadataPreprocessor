# Analysis

Script to generate the gcode metadata.

## Installation

```
$ mkdir -p ~/.Slic3r/utils/gcode_metadata
$ cd ~/.Slic3r/utils/gcode_metadata
$ wget https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/master.zip
$ unzip -j master.zip "OctoPrint-MetadataPreprocessor-master/analysis/*" -d .
$ virtualenv -p /usr/bin/python2 venv
$ source venv/bin/activate
$ python setup.py install
```

## Usage

```
$ analysis --help
Usage: analysis [OPTIONS] PATH

Options:
  --speed-x FLOAT
  --speed-y FLOAT
  --offset <FLOAT FLOAT>...
  --max-t INTEGER
  --g90-extruder
  --help                     Show this message and exit.
```

## Slic3r

You can easily integrate the analysis script in your workflow with slic3r. Simply add the absolute path of the script under the [post-processing scripts](http://manual.slic3r.org/advanced/post-processing) option.

![Screenshot](https://raw.githubusercontent.com/malnvenshorn/OctoPrint-MetadataPreprocessor/master/docs/slic3r.png)

If you want to supply arguments, e.g. `--g90-extruder`, you need to write a wrapper script. I placed mine under `~/.Slic3r/utils/gcode_metadata/generate_octoprint_metadata.sh`, see screenshot above.

```
#!/bin/bash

~/scripts/gcode_metadata/venv/bin/analysis --g90-extruder "$@"
```
