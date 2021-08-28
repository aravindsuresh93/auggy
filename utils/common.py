import os
import cv2

def convert_to_auggy(cls_obj):
    auggy_dict = cls_obj.__dict__
    auggy_dict['bounding_box'] = [b.__dict__ for b in auggy_dict['bounding_box']]
    return auggy_dict

def get_image_info(fpath, image_folder, image_formats):
    name = os.path.basename(fpath).split('.txt')[0]
    images = os.listdir()
    for extenstion in image_formats:
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