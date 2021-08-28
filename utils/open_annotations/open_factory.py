class OpenAnnotations:
    def get(self, format):
        if format == ".xml":
            from utils.open_annotations.open_pascal import OpenXMLFile
            return OpenXMLFile()
        elif format == ".txt":
            from utils.open_annotations.open_yolo import OpenTextFile
            return OpenTextFile()
        else:
            raise NotImplementedError("Annotation Format not supported")

class OpenLabels:
    def get(self, format, file = ""):
        if format == ".xml":
            return {}
        elif format == ".txt":
            from utils.common import YoloLabels
            return YoloLabels(self.PF.classesPath).classes



            