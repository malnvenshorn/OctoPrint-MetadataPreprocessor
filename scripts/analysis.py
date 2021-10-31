#!/usr/bin/env python

__version__ = "0.3.0"

import logging
import os
import shutil
import sys
import time
import yaml
import click

from copy import deepcopy
from tempfile import NamedTemporaryFile as tempfile
from urllib.error import URLError
from urllib.request import urlopen, Request
from yaml import YAMLError

workingDirectory = os.getcwd()
scriptDirectory = os.path.dirname(os.path.realpath(__file__))

logFile = 'analysis.log'
configFile = 'update.yaml'

defaultConfig = {
    'enable': True,
    'interval': 24,
    'last_check': 0,
    'file': {
        'analysis.py': {
            'hash': '',
            'check_url': 'https://api.github.com/repos/malnvenshorn/OctoPrint-MetadataPreprocessor/contents/scripts/analysis.py',  # noqa
        },
        'gcodeInterpreter.py': {
            'hash': '',
            'check_url': 'https://api.github.com/repos/octoprint/octoprint/contents/src/octoprint/util/gcodeInterpreter.py',  # noqa
        },
    },
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(scriptDirectory, logFile)),
        logging.StreamHandler(sys.stdout)
    ]
)


def dict_merge(a, b):
    """
    Recursively merges two dictionaries.
    """
    result = deepcopy(a)

    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def load_config():
    try:
        logging.debug(f"Loading config file '{configFile}'")
        with open(os.path.join(scriptDirectory, configFile)) as file:
            userConfig = yaml.safe_load(file)
    except FileNotFoundError:
        logging.info(f"Config file '{configFile}' not found, using defaults")
        userConfig = {}
    except Exception as e:
        logging.error(f"Failed to read config file '{configFile}' - {str(e)}")
        userConfig = {'enable': False}

    return dict_merge(defaultConfig, userConfig)


def save_config(config):
    try:
        logging.debug(f"Saving config file '{configFile}'")
        with open(os.path.join(scriptDirectory, configFile), mode='w') as file:
            file.write(yaml.dump(config, indent=2))
    except Exception as e:
        logging.error(f"Failed to save config file '{configFile}' - {str(e)}")


def get_file_info(name, config):
    try:
        url = config['file'][name]['check_url']
        logging.debug(f"Querying update information for file '{name}' using {url}")
        request = Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
        with urlopen(request) as response:
            result = yaml.safe_load(response.read().decode())
            return result['sha'], result['download_url']
    except URLError as e:
        logging.error(f"Failed to query update information for file '{name}' - {str(e)}")
    except YAMLError as e:
        logging.error(f"Failed to parse update information for file '{name}' - {str(e)}")


def update_file(name, url):
    try:
        logging.debug(f"Downloading '{name}' from {url}")
        with (urlopen(url) as response,
              open(os.path.join(scriptDirectory, name), mode='wb') as file):
            shutil.copyfileobj(response, file)
        return True
    except Exception as e:
        logging.error(f"Failed to download file '{name}' - {str(e)}")
        return False


def perform_restart(recompile=False):
    logging.info("Restarting script")
    if recompile:
        from py_compile import compile
        compile(os.path.join(scriptDirectory, 'gcodeInterpreter.py'))
    args = sys.argv[:]
    args.insert(0, sys.executable)
    os.chdir(workingDirectory)
    os.execv(sys.executable, args)


def self_update(config):
    if not config['enable']:
        logging.info("Update is disabled")
        return

    restart = False
    timestamp = time.time()

    if timestamp - config['last_check'] > config['interval'] * 60 * 60:
        logging.info("Checking for updates")
        for file in config['file']:
            hash, downloadUrl = get_file_info(file, config)
            if hash is not None and hash != config['file'][file]['hash']:
                logging.info(f"Updating '{file}'")
                result = update_file(file, downloadUrl)
                restart = restart or result
                if result:
                    config['file'][file]['hash'] = hash
        config['last_check'] = timestamp

    save_config(config)

    if restart:
        perform_restart(True)


def gcode_analysis(path, speedx, speedy, offsets, max_extruders, g90_extruder):
    try:
        from gcodeInterpreter import gcode
    except ImportError:
        logging.critical(
            "The 'gcodeInterpreter.py' file is missing. That file is required for this script to work. Please enable "
            "the auto update or download it manually from the OctoPrint source and place it in the same directory as "
            "this script. More information can be found in the wiki at "
            "https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/wiki")
        exit(1)

    fileName = os.path.basename(path)

    logging.info(f"Starting analysis of '{fileName}'")

    start_time = time.time()

    interpreter = gcode()

    interpreter.load(path,
                     speedx=speedx,
                     speedy=speedy,
                     offsets=list(offsets),
                     max_extruders=max_extruders,
                     g90_extruder=g90_extruder)

    ystr = yaml.safe_dump(interpreter.get_result(), default_flow_style=False, indent=2, allow_unicode=True)

    with open(path) as fsrc, tempfile(mode='w', delete=False) as fdst:
        fdst.write(';OCTOPRINT_METADATA\n')
        for line in ystr.splitlines():
            fdst.write(f';{line}\n')
        fdst.write(';OCTOPRINT_METADATA_END\n')
        fdst.write('\n')
        chunk_size = 1024 * 1024 * 10  # 10MB
        shutil.copyfileobj(fsrc, fdst, length=chunk_size)

    shutil.move(fdst.name, path)

    logging.info(f"Analysis of '{fileName}' finished in {time.time() - start_time :.2f}s")


@click.command()
@click.option('--verbose', 'verbose', is_flag=True)
@click.option('--speed-x', 'speedx', type=float, default=6000)
@click.option('--speed-y', 'speedy', type=float, default=6000)
@click.option('--offset', 'offsets', type=(float, float), multiple=True)
@click.option('--max-extruders', 'max_extruders', type=int, default=10)
@click.option('--g90-extruder', 'g90_extruder', is_flag=True)
@click.argument('path', type=click.Path(exists=True))
def main(verbose, path, **gcodeParamater):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.info(f"Running script version {__version__}")
    config = load_config()
    self_update(config)
    gcode_analysis(path, **gcodeParamater)


if __name__ == '__main__':
    main()
