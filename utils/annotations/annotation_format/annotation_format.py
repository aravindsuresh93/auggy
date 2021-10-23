import os

SUPPORTED_EXTENSIONS = [".txt", ".xml"]

class FormatFinder:
    @staticmethod
    def get_formats(annotation_folder):
        formats = {}
        files = os.listdir(annotation_folder)
        for f in files:
            extension = os.path.splitext(f)[1]
            if extension in SUPPORTED_EXTENSIONS:
                formats[extension] = 1
        formats = list(formats.keys())
        return formats
