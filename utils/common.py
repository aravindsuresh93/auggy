import os
import cv2

def skip_files(file_name):
    if file_name == 'classes.txt':
        return True
    if ".DS_Store" in file_name:
        return True
    return False

def convert_to_auggy(cls_obj):
    auggy_dict = cls_obj.__dict__
    if len(auggy_dict.get("error", "")):
        return auggy_dict
    auggy_dict['bounding_box'] = [b.__dict__ for b in auggy_dict['bounding_box']]
    return auggy_dict


IMAGE_FORMATS = ["jpg", "jpeg", "png"]
def get_image_info(image_folder, name):
    images = os.listdir(image_folder)
    for extenstion in IMAGE_FORMATS:
        if f'{name}.{extenstion}' in images:
            ipath = os.path.join(image_folder, f'{name}.{extenstion}')
            height, width, depth = cv2.imread(ipath).shape
            return ipath, height, width, depth
    return '', 0, 0, 0


class YoloLabels:
    def __init__(self, artefacts_path):
        files = os.listdir(artefacts_path)
        assert len(files), "labels file for YoloFormat not found, kindly upload"
        cpath = ""
        for f in files:
            basename, ext = os.path.splitext(f)
            if ext in ['.names', '.label', '.txt']:
                cpath = os.path.join(artefacts_path, f)
                break
        
        assert len(cpath), "labels file for YoloFormat not found, kindly upload"
        with open(cpath, 'r') as f:
            labels = f.readlines()

        self.classes = {}
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            self.classes[e] = label


class EmtpyLabels:
    def __init__(self, cpath):
        self.classes = {}