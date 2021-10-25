from octoprint.plugin import OctoPrintPlugin

from .analysis import MetadataAnalysisQueue


class MetadataPreprocessorPlugin(OctoPrintPlugin):

    # Analysis Queue

    def get_analysis_queue(self):
        return dict(gcode=MetadataAnalysisQueue)

    # Software Update

    def get_update_information(self):
        return {
            self._identifier: dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="malnvenshorn",
                repo="OctoPrint-MetadataPreprocessor",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/malnvenshorn/OctoPrint-MetadataPreprocessor/archive/{target_version}.zip",
            )
        }


__plugin_name__ = "Metadata Preprocessor"

__plugin_pythoncompat__ = ">=3.7"

__plugin_implementation__ = MetadataPreprocessorPlugin()

__plugin_hooks__ = {
    "octoprint.filemanager.analysis.factory": __plugin_implementation__.get_analysis_queue,
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
}
