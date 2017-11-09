# OctoPrint-MetadataPreprocessor

This OctoPrint plugin uses metadata comments in gcode files to speed up the analyzing process on systems with limited resources like the Raspberry PI.

Just as an Example: Analyzing a 7MB gcode file on my Raspberry PI B+ took ~17min. With included metadata only 2s while generating the metadata itself took additional 8s on my laptop.

Currently it's just meant for testing and not for productional use.

## How it works

The script inside the _analysis_ directory uses OctoPrint's gcode interpreter to analyze the given gcode file. After the analysis has finished the metadata is written to the beginning of the file.

The plugin stops every gcode analysis started by OctoPrint and looks weather the file contains such metadata or not. If metadata is found it will be added to the _.metadata.yaml_ and the _METADATA&#95;ANALYSIS&#95;FINISHED_ event will be fired. Otherwise the file will be analyzed by OctoPrint as usual by adding it to the analysis queue again.

## Installation

You can install this plugin manually using this URL:

```
https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/master.zip
```
