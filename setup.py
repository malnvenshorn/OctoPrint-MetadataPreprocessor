import os

from setuptools import find_packages
from setuptools import setup

plugin_name = "OctoPrint-MetadataPreprocessor"
plugin_description = "Read metadata block from gcode files to speed up the analyzing process."
plugin_version = "0.1.0"
plugin_author = "Sven Lohrmann"
plugin_author_email = "malnvenshorn@mailbox.org"
plugin_url = "https://github.com/malnvenshorn/octoprint-metadatapreprocessor"
plugin_license = "AGPLv3"
plugin_identifier = "metadatapreprocessor"
plugin_package = "octoprint_metadatapreprocessor"
plugin_source_folder = "src"
plugin_requires = [
    "OctoPrint"
]

try:
    import octoprint_setuptools
except ImportError:
    print("Could not import OctoPrint's setuptools, are you sure you are running that under "
          "the same python installation that OctoPrint is installed under?")
    import sys
    sys.exit(-1)

cmdclass = dict()

translation_dir = os.path.join('.', "translations")
pot_file = os.path.join(translation_dir, "messages.pot")

cmdclass.update(
    octoprint_setuptools.get_babel_commandclasses(
        pot_file=pot_file,
        output_dir=translation_dir,
        bundled_dir=None,
        pack_name_prefix=f"{plugin_name}-i18n-",
        pack_path_prefix=f"_plugins/{plugin_identifier}/",
    )
)

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    author_email=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    # Adding new commands
    cmdclass=cmdclass,
    # List of our packages
    packages=find_packages(where=plugin_source_folder, exclude=["*analysis"]),
    # Map package to directory names
    package_dir={"": plugin_source_folder},
    # Include additional data files that are specified in the MANIFEST.in file
    include_package_data=True,
    # We have package data that needs to be accessible on the file system, such as templates or static assets
    # therefore this plugin is not zip_safe.
    zip_safe=False,
    install_requires=plugin_requires,
    # Hook the plugin into the "octoprint.plugin" entry point, mapping the plugin_identifier to the plugin_package.
    # That way OctoPrint will be able to find the plugin and load it.
    entry_points={
        "octoprint.plugin": [f"{plugin_identifier} = {plugin_package}"],
    },
)
