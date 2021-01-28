import albumentations as A
from matplotlib import pyplot as plt
import random
import cv2
import os

# class Augment:
#     def __init__(self, annotation_type):
#         self.annotation_type = annotation_type

#     def transform()

cpath = r"C:\Users\ds\Desktop\Projects\test_images\yolo\classes.txt"
ipath = r"C:\Users\ds\Desktop\Projects\test_images\yolo\JIY4434.jpg"
tpath = r"C:\Users\ds\Desktop\Projects\test_images\yolo\JIY4434.txt"

"""Bounding Box Class"""
class BoundingBoxTXT:
    def __init__(self, label, xmin, ymin, xmax, ymax):
        self.label = label
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.h = ymax - ymin
        self.w = xmax - xmin

"""Converts TXT into unified class object"""
class TextFile:
    def __init__(self, classes, lines, ipath, fpath, width, height, depth):
        self.image_name = os.path.basename(ipath)
        self.image_path = ipath
        self.path = fpath
        self.width = width
        self.height = height
        self.depth = depth
        self.bbox = []
        for line in lines:
            line = line.strip()
            data = line.split()
            label = classes[int(data[0])]
            bbox_width = float(data[3]) * width
            bbox_height = float(data[4]) * height
            center_x = float(data[1]) * width
            center_y = float(data[2]) * height
            xmin = int(center_x - (bbox_width / 2))
            ymin = int(center_y - (bbox_height / 2))
            xmax = int(center_x + (bbox_width / 2))
            ymax = int(center_y + (bbox_height / 2))
            
            self.bbox.append(BoundingBoxTXT(label, xmin, ymin, xmax, ymax))


class TxtExtract:

    def load_classes(self):
        with open(r"C:\Users\ds\Desktop\Projects\test_images\yolo\classes.txt", 'r') as f:
            labels = f.readlines()

        self.classes = {}
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            self.classes[e] = label

    def get_corr_image(self, fpath):
        name = os.path.basename(fpath)
        name = name.split('.txt')[0]
        images = os.listdir(r"C:\Users\ds\Desktop\Projects\test_images\yolo")
        found = 0
        for fformat in ['jpg']:
            image_name = f'{name}.{fformat}'
            if image_name in images:
                found = 1
                break
        if found:
            ipath = os.path.join(r"C:\Users\ds\Desktop\Projects\test_images\yolo", image_name)
            img = cv2.imread(ipath)
            height, width, depth = img.shape
            return ipath, height, width, depth
        return '', 0, 0, 0

    def extract(self, fpath):
        self.load_classes()
        with open(fpath, 'r') as f:
            lines = f.readlines()
        ipath, height, width, depth = self.get_corr_image(fpath)

        masterDict = {}
        TFile = TextFile(self.classes, lines, ipath, fpath, width, height, depth)
        masterDict.update({'path': TFile.path, 'image_name': TFile.image_name,
                            'image_path': TFile.image_path, 'height': TFile.height,
                            'width': TFile.width, 'depth': TFile.depth})

        for att in TFile.bbox:
            attval = masterDict.get(att.label, 0)
            attval += 1
            masterDict.update({att.label: attval})
        return masterDict, TFile


def convert_to_aub(txt_obj):
    boxes = []
    for box in txt_obj.bbox:
        boxes.append([box.xmin, box.ymin, box.xmax,box.ymax, box.label])
    return boxes
        



TE = TxtExtract()
f, tobj = TE.extract(tpath)

boxes = convert_to_aub(tobj)


transform = A.Compose(
    [ A.ShiftScaleRotate(p=0.5)],
    bbox_params=A.BboxParams(format='pascal_voc'),
)
image = cv2.imread(ipath)
transformed = transform(image=image, bboxes=boxes)

print(transformed)


