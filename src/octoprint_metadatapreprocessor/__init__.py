# coding=utf-8
from __future__ import absolute_import

__author__ = "Sven Lohrmann <malnvenshorn@mailbox.org>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 Sven Lohrmann - Released under terms of the AGPLv3 License"

import io
import yaml

import octoprint.plugin
from octoprint.events import Events


class MetadataPreprocessorPlugin(octoprint.plugin.EventHandlerPlugin):

    def __init__(self):
        self.queue = []

    # EventHandlerPlugin

    def on_event(self, event, payload):
        if event == Events.METADATA_ANALYSIS_STARTED:
            self.on_analysis_started(payload)

    def on_analysis_started(self, payload):
        location = payload["origin"]
        path = payload["path"]

        queue_entry = self._file_manager._analysis_queue_entry(location, path)

        if queue_entry in self.queue:
            # Do nothing if we added the queue entry
            self.queue.remove(queue_entry)
            return

        self._logger.info("Aborting analysis of {entry}".format(entry=queue_entry))
        self._analysis_queue.dequeue(queue_entry)

        self._logger.info("Looking for metadata in {entry}".format(entry=queue_entry))
        path_on_disk = self._file_manager.path_on_disk(location, path)
        analysis = self.read_metadata_from_file(path_on_disk)

        if analysis is None:
            self._logger.info("Requeuing {entry} for analysis by octoprint"
                              .format(entry=queue_entry))
            self.queue.append(queue_entry)
            self._analysis_queue.enqueue(queue_entry, high_priority=True)
        else:
            self._logger.info("Using found metadata from {entry}".format(entry=queue_entry))
            self._analysis_queue._analysis_finished(queue_entry, analysis)
            self._file_manager._add_analysis_result(location, path, analysis)

    def read_metadata_from_file(self, path):
        def strip_comment(string):
            return string[string.find(";")+1:] if ";" in string else ""

        with io.open(path, encoding="utf-8", errors="replace") as file_stream:
            line = strip_comment(file_stream.readline())

            if not line.startswith("OCTOPRINT_METADATA"):
                self._logger.info("Metadata tag not found at the beginning of the file")
                return

            metadata = []

            max_lines = 100
            line_no = 1

            for line in file_stream:
                line_no += 1
                line = strip_comment(line)
                if line.startswith("OCTOPRINT_METADATA_END"):
                    break
                elif line_no >= max_lines:
                    self._logger.warn("Expecting metadata end tag within {no} lines".format(no=max_lines))
                    return
                else:
                    metadata.append(line)

            try:
                analysis = yaml.safe_load("".join(metadata))
                result = dict()
                result["printingArea"] = analysis["printing_area"]
                result["dimensions"] = analysis["dimensions"]
                if analysis["total_time"]:
                    result["estimatedPrintTime"] = analysis["total_time"] * 60
                if analysis["extrusion_length"]:
                    result["filament"] = dict()
                    for i in xrange(len(analysis["extrusion_length"])):
                        result["filament"]["tool%d" % i] = {
                            "length": analysis["extrusion_length"][i],
                            "volume": analysis["extrusion_volume"][i]
                        }
                return result
            except yaml.YAMLError as e:
                self._logger.warn("Malformed metadata: {error}".format(error=str(e)))
            except KeyError as e:
                self._logger.warn("Missing property {key} in metadata".format(key=str(e)))

    # Softwareupdate hook

    def get_update_information(self):
        return dict(
            metadatapreprocessor=dict(
                displayName="Metadata Preprocessor",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="malnvenshorn",
                repo="OctoPrint-MetadataPreprocessor",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/{target_version}.zip"
            )
        )


__plugin_name__ = "Metadata Preprocessor"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MetadataPreprocessorPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
