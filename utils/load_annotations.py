from utils.open_annotations.open_factory import OpenAnnotations, OpenLabels
import os

class LoadAnnotations:
    def __init__(self):
        self.annotation_info = {}

    def load(self, base_directory, annotation_format):
        self.annotation_info = {}
        annotation_files = [file for file in os.listdir(base_directory) if annotation_format in file]
        
        AE = OpenAnnotations.get(annotation_format)
        classes = OpenLabels.get(annotation_format)
        for file in annotation_files:
            if file == 'classes.txt': continue
            annotation = AE.open(os.path.join(base_directory, file), classes)
            self.annotation_info[file] = annotation


