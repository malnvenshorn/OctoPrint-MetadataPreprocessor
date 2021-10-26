@echo off
python %APPDATA%\Slic3r\scripts\gcode_metadata\analysis.py --g90-extruder "%*"
