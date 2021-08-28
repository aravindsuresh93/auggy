class OpenAnnotations:
    @staticmethod
    def get(format):
        if format == ".xml":
            from utils.open_annotations.open_pascal import OpenXMLFile
            return OpenXMLFile()
        elif format == ".txt":
            from utils.open_annotations.open_yolo import OpenTextFile
            return OpenTextFile()
        else:
            raise NotImplementedError("Annotation Format not supported")

class OpenLabels:
    @staticmethod
    def get(format, fpath = ""):
        if format == ".xml":
            return {}
        elif format == ".txt":
            from utils.common import YoloLabels
            return YoloLabels(fpath).classes



            