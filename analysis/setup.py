# coding=utf-8
from __future__ import absolute_import

__author__ = "Sven Lohrmann <malnvenshorn@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 Sven Lohrmann - Released under terms of the AGPLv3 License"

from setuptools import setup

setup(
    name="analysis",
    version="0.1",
    py_modules=["analysis"],
    install_requires=[
        "Click>=6.2,<6.3",
        "PyYAML>=3.10,<3.11",
    ],
    entry_points="""
        [console_scripts]
        analysis=analysis:gcode_analysis
    """,
)
