#!/usr/bin/env python

import os
import shutil
import time
import yaml
import click

from tempfile import NamedTemporaryFile as tempfile
from urllib import request

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
interpreterUrl = "https://github.com/OctoPrint/OctoPrint/raw/master/src/octoprint/util/gcodeInterpreter.py"


def update_interpreter():
    with (request.urlopen(interpreterUrl) as response,
          open(os.path.join(scriptDirectory, "gcodeInterpreter.py"), mode="wb") as file):
        shutil.copyfileobj(response, file)


try:
    from gcodeInterpreter import gcode
except ImportError:
    try:
        update_interpreter()
        from gcodeInterpreter import gcode
    except Exception:
        click.echo(
            "Failed to download gcodeInterpreter.py from the OctoPrint source. That file is required for this script "
            "to work. Please download it manually and place it in the same directory as this script. The file can "
            "be found at: " + interpreterUrl,
            err=True)
        exit(1)


@click.command()
@click.option("--speed-x", "speedx", type=float, default=6000)
@click.option("--speed-y", "speedy", type=float, default=6000)
@click.option("--offset", "offset", type=(float, float), multiple=True)
@click.option("--max-t", "maxt", type=int, default=10)
@click.option("--g90-extruder", "g90_extruder", is_flag=True)
@click.argument("path", type=click.Path(exists=True))
def gcode_analysis(path, speedx, speedy, offset, maxt, g90_extruder):
    offsets = offset
    if offsets is None:
        offsets = []
    elif isinstance(offset, tuple):
        offsets = list(offsets)
    offsets = [(0, 0)] + offsets
    if len(offsets) < maxt:
        offsets += [(0, 0)] * (maxt - len(offsets))

    start_time = time.time()

    interpreter = gcode()

    interpreter.load(path,
                     speedx=speedx,
                     speedy=speedy,
                     offsets=offsets,
                     max_extruders=maxt,
                     g90_extruder=g90_extruder)

    ystr = yaml.safe_dump(interpreter.get_result(), default_flow_style=False, indent=2, allow_unicode=True)

    with open(path) as fsrc, tempfile(mode="w", delete=False) as fdst:
        fdst.write(";OCTOPRINT_METADATA\n")
        for line in ystr.splitlines():
            fdst.write(f";{line}\n")
        fdst.write(";OCTOPRINT_METADATA_END\n")
        fdst.write("\n")
        chunk_size = 1024 * 1024 * 10  # 10MB
        shutil.copyfileobj(fsrc, fdst, length=chunk_size)

    shutil.move(fdst.name, path)

    click.echo(f"Finished in {time.time() - start_time :.2f}s")


if __name__ == '__main__':
    gcode_analysis()
