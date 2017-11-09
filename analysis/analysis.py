# coding=utf-8
from __future__ import absolute_import

__author__ = "Sven Lohrmann <malnvenshorn@gmail.com> based on work from Gina Häußge <osd@foosel.net>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 Sven Lohrmann - Released under terms of the AGPLv3 License"

import shutil
import time
import yaml
import click
from tempfile import NamedTemporaryFile as tempfile
from gcodeInterpreter import gcode


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

    ystr = yaml.safe_dump(interpreter.get_result(), default_flow_style=False, indent="    ", allow_unicode=True)

    with open(path) as fsrc, tempfile(delete=False) as fdst:
        fdst.write(";OCTOPRINT_METADATA\n")
        for line in ystr.splitlines():
            fdst.write(";{}\n".format(line))
        fdst.write(";OCTOPRINT_METADATA_END\n")
        fdst.write("\n")
        chunk_size = 1024 * 1024 * 10  # 10MB
        shutil.copyfileobj(fsrc, fdst, length=chunk_size)

    shutil.move(fdst.name, path)

    click.echo("Finished in {}s".format(time.time() - start_time))
