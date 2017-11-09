# Analysis

Script to analyze the gcode and to add the metadata to the beginning of the file.

## Installation

```
$ wget https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/master.zip
$ unzip -j master.zip "OctoPrint-MetadataPreprocessor-master/analysis/*" -d analysis
$ cd analysis
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

You can easily integrate the analysis script in your workflow with slic3r. Simply add the absolute path of the script under the [post-processing scripts](http://manual.slic3r.org/advanced/post-processing) option. The absolute path of the generated gcode file will automatically passed to the script. If you want to supply arguments, e.g. `--g90-extruder`, you need to write a wrapper script.
