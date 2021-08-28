from utils.open_annotations.open_factory import OpenAnnotations, OpenLabels
from utils.common import skip_files
import pandas as pd
import os


class LoadAnnotations:
    """
    Load annotationfiles and convert them into standardized dataframe
    """
    @staticmethod
    def combine_annotation_to_frame(annotation_info):
        df = pd.DataFrame()   
        for f, info in annotation_info.items():
            if len(info.get("error", "")):
                sdf = pd.DataFrame(info, [0])
                df = df.append(sdf) if len(df) else  sdf
            main_info = info.copy()
            if 'bounding_box' in main_info.keys(): main_info.pop('bounding_box')
            for bbox in info.get('bounding_box', []):
                combined = {**main_info, **bbox}
                sdf = pd.DataFrame(combined, [0])
                df = df.append(sdf) if len(df) else  sdf
        df['error'] = 0 if "error" not in df.columns else df['error'].fillna(0)
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def convert_classes_to_frame(classes):
        return pd.DataFrame.from_dict(classes, orient = 'index')

    @staticmethod
    def load(annotation_folder, annotation_format, image_folder, classes_path=""):
        annotation_info = {}
        annotation_files = [file for file in os.listdir(annotation_folder) if annotation_format in file]
        AE = OpenAnnotations.get(annotation_format)
        classes = OpenLabels.get(annotation_format, classes_path)
        for file_name in annotation_files:
            if skip_files(file_name): continue
            name = file_name.split(annotation_format)[0]
            annotation = AE.open(os.path.join(annotation_folder, file_name), image_folder, name, classes)
            annotation_info[file_name] = annotation
        df = LoadAnnotations.combine_annotation_to_frame(annotation_info)
        classes = LoadAnnotations.convert_classes_to_frame(classes)
        return df, classes






