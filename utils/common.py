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
    def __init__(self, cpath):
        with open(cpath, 'r') as f:
            labels = f.readlines()

        self.classes = {}
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            self.classes[e] = label