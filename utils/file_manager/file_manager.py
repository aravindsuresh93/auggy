from utils.load_annotations import LoadAnnotations
from clogger.clogger import CLogger
from config.config import BASE_FOLDER
import shutil
import os

logger = CLogger.get("auggy-file-manager")

class FileManager:
    @staticmethod
    def __upload(files, save_folder):
        logger.info(f"Uploading files to {save_folder}")
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

    def upload_build(projectname):
        logger.info(f"Loading project {projectname}")
        return LoadAnnotations.load(projectname)
