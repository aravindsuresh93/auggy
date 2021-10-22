import shutil
import os

BASE_FOLDER = "data_lake"

class FileManager:
    @staticmethod
    def __upload(files, save_folder):
        try:
            for file in files:
                with open(os.path.join(save_folder, file.filename), "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
            return 0,""
        except Exception as e:
            return 1, e

    @staticmethod
    def upload_images(projectname, files):
        return FileManager.__upload(files, f'{BASE_FOLDER}/{projectname}/input_images')

    @staticmethod
    def upload_annotations(projectname, files):
        return FileManager.__upload(files, f'{BASE_FOLDER}/{projectname}/input_annotations')

    @staticmethod
    def upload_artefacts(projectname, files):
        return FileManager.__upload(files, f'{BASE_FOLDER}/{projectname}/artefacts') 