# OctoPrint-MetadataPreprocessor

This OctoPrint plugin uses a generated metadata comment in the gcode file to speed up the analyzing process on systems with limited resources like the Raspberry PI.

As an example: Analyzing a 7MB gcode file on my Raspberry PI B+ took ~17min. With included metadata only 2s while generating the metadata itself took additional 8s on my laptop.

## How it works

The separate analysis script uses OctoPrint's gcode interpreter to analyze the given gcode file. After the analysis has finished the metadata is written to the beginning of the file.

If the gcode is uploaded the plugin stops the gcode analysis started by OctoPrint and looks whether the file contains such metadata or not. If metadata is found it will be added to the `.metadata.yaml` and the `_METADATA_ANALYSIS_FINISHED_` event will be fired. Otherwise the file will be analyzed by OctoPrint as usual by adding it to the analysis queue again.

## Installation

To install the analysis script go to the [wiki](https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/wiki).

The OctoPrint plugin can be installed via the bundled Plugin Manager or manually using this URL:

```
https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/master.zip
```