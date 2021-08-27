
class OpenAnnotations:
    def get(self, format):
        if format == ".xml":
            from utils.open_annotations.open_pascal import OpenXMLFile
            return OpenXMLFile
        if format == ".txt":
            from utils.open_annotations.open_yolo import OpenTextFile
            return OpenTextFile


            