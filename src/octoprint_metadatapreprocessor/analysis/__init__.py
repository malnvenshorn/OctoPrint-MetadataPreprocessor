import yaml

from octoprint.filemanager.analysis import GcodeAnalysisQueue

from .utils import strip_comment


class MetadataAnalysisQueue(GcodeAnalysisQueue):
    def __init__(self, finishedCallback):
        super().__init__(finishedCallback)

    def _do_analysis(self, high_priority=False):
        entry = self._current

        self._logger.info(f"Looking for metadata in {entry}")

        result = self.read_metadata_from_file(entry.absolute_path)

        if result is None:
            self._logger.info(f"Passing {entry} to OctoPrint's analysis queue")
            return super()._do_analysis(high_priority)
        else:
            self._logger.info(f"Using found metadata from {entry}")
            return result

    def read_metadata_from_file(self, path):
        with open(path, encoding="utf-8", errors="replace") as file:
            line = strip_comment(file.readline())

            if not line.startswith("OCTOPRINT_METADATA"):
                self._logger.info("Metadata tag not found at the beginning of the file")
                return

            metadata = []

            maxLineLookup = 100
            lineCount = 1

            for line in file:
                lineCount += 1
                line = strip_comment(line)
                if line.startswith("OCTOPRINT_METADATA_END"):
                    break
                elif lineCount >= maxLineLookup:
                    self._logger.warn(f"Expecting metadata end tag within {maxLineLookup} lines")
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
                    for i in range(len(analysis["extrusion_length"])):
                        result["filament"][f"tool{i}"] = {
                            "length": analysis["extrusion_length"][i],
                            "volume": analysis["extrusion_volume"][i]
                        }
                return result
            except yaml.YAMLError as e:
                self._logger.warn(f"Malformed metadata: {str(e)}")
            except KeyError as e:
                self._logger.warn(f"Missing property {str(e)} in metadata")
