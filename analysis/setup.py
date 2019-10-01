# coding=utf-8
from __future__ import absolute_import

__author__ = "Sven Lohrmann <malnvenshorn@mailbox.org>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 Sven Lohrmann - Released under terms of the AGPLv3 License"

from setuptools import setup

setup(
    name="analysis",
    version="0.1",
    py_modules=["analysis", "gcodeInterpreter"],
    install_requires=[
        "Click>=7,<8",
        "PyYAML>=5.1,<6",
    ],
    entry_points="""
        [console_scripts]
        analysis=analysis:gcode_analysis
    """,
)
