# OctoPrint-MetadataPreprocessor

This OctoPrint plugin reads a generated metadata block in the gcode file to speed up the analyzing process on systems with limited resources like the Raspberry PI.

As an example: Analyzing a 7MB gcode file on my Raspberry PI B+ took ~17min. With included metadata only 2s while generating the metadata itself took additional 8s on my laptop.

## How it works

The separate analysis script uses OctoPrint's gcode interpreter to analyze the given gcode file. After the analysis has finished the metadata is written to the beginning of the file.

If you upload this file to OctoPrint it will be added to the plugins own implementation of the analyses queue. If a valid metadata block is found the analyses is done. Otherwise the file will be passed on to OctoPrint's default queue and analyzed as usual.

## Installation

This plugin can be installed ~~via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) or~~ manually using the URL below. More information on how to install a plugin can be found on the [OctoPrint website](https://plugins.octoprint.org/help/installation/).

```
https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/master.zip
```

Instructions on how to setup the analysis script can be found in the [wiki](https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/wiki).
