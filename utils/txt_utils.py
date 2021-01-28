from utils.path_manager import PathFinder
import numpy as np
import json
import os
import cv2


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
    def __init__(self):
        self.PF = PathFinder()
        self.PF.load()

    def load_classes(self):
        with open(self.PF.classesPath, 'r') as f:
            labels = f.readlines()

        self.classes = {}
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            self.classes[e] = label

    def get_corr_image(self, fpath):
        name = os.path.basename(fpath)
        name = name.split('.txt')[0]
        images = os.listdir(self.PF.imageFolder)
        found = 0
        for fformat in self.PF.imgFormat:
            image_name = f'{name}.{fformat}'
            if image_name in images:
                found = 1
                break
        if found:
            ipath = os.path.join(self.PF.imageFolder, image_name)
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


class EditClasses:
    def rename(self, oldname, newname):
        self.PF = PathFinder()
        self.PF.load()
        with open(self.PF.classesPath, 'r') as f:
            labels = f.readlines()
        new_labels = []
        change = False
        for label in labels:
            label = label.replace('\n', '')
            if label == oldname:
                new_labels.append(newname)
                change = True
            else:
                new_labels.append(label)

        if change:
            with open(self.PF.classesPath, 'w') as f:
                pass

            for label in new_labels:
                with open(self.PF.classesPath, 'a') as f:
                    f.write(label + '\n')


class DeleteClass:
    def delete(self, oldnames):
        """creationm"""
        self.PF = PathFinder()
        self.PF.load()
        with open(self.PF.classesPath, 'r') as f:
            labels = f.readlines()

        current_classes = {}
        modified_labels = []
        modified_classes = {}
        deleted_labels = []
        
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            current_classes[str(e)] = label
            if label in oldnames:
                deleted_labels.append(label)
            else:
                modified_classes[str(len(modified_labels))] = label
                modified_labels.append(label)

        modified_classes = { str(v) : str(k) for k,v in modified_classes.items()}

        """refresh"""

        for file in os.listdir(self.PF.annotationFolder):
            if not self.PF.annotationFormat in file or file == 'classes.txt' or '.DS' in file:
                continue

            fpath = os.path.join(self.PF.annotationFolder, file)
            with open(fpath, 'r') as f:
                lines = f.readlines()

            texts = []
            for line in lines:
                line = line.strip()
                data = line.split()
                val = data[0]
                label = current_classes[str(val)]
                new_val = modified_classes.get(label, None)

                if new_val:
                    texts.append(f'{new_val} {data[1]} {data[2]} {data[3]} {data[4]}')
                else:
                    print(label)

            with open(fpath, 'w') as f:
                pass

            for text in texts:
                with open(fpath, 'a') as f:
                    f.write(text + '\n')

        with open(self.PF.classesPath, 'w') as f:
            pass

        for label in modified_labels:
            with open(self.PF.classesPath, 'a') as f:
                f.write(label + '\n')

def convert_to_yolo(W,H, xmin, ymin,xmax, ymax):
    dw = 1./W
    dh = 1./H 
    x = (xmin + xmax)/2.0
    y = (ymin+ ymax)/2.0
    w = xmax-xmin
    h = ymax-ymin
    x = round(x*dw,6)
    w = round(w*dw,6)
    y = round(y*dh,6)
    h = round(h*dh,6)
    return x,y,w,h

class EditTextFile:
    def __init__(self):
        self.TE = TxtExtract()
        self.convert_to_idx()
        self.PF = PathFinder()
        
    def get_bounding_boxes(self,txt_path):
        _, self.text_file  = self.TE.extract(txt_path)
        original_boxes, names = [], []
        for e, box in enumerate(self.text_file.bbox):
            bbox = np.array([box.xmin,box.ymin, box.xmax, box.ymax, e])
            original_boxes.append(bbox)
            names.append(box.label)
        return original_boxes, names

    def convert_to_idx(self):
        """creationm"""
        self.PF.load()
        with open(self.PF.classesPath, 'r') as f:
            labels = f.readlines()

        classes,self.inv_classes = {}, {}
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            classes[str(e)] = label
        self.inv_classes = { str(v) : str(k) for k,v in classes.items()}

    def write(self, newbboxes, names,H, W,out_path):
        with open(out_path, 'w') as f:
                pass

        texts = []
        for box in newbboxes:
            xmin, ymin, xmax, ymax, c =  box
            name = names[c]
            idx = self.inv_classes[name]
            x,y,w,h = convert_to_yolo(W,H, xmin, ymin,xmax, ymax)
            texts.append(f'{idx} {x} {y} {w} {h}')


        for text in texts:
            with open(out_path, 'a') as f:
                f.write(text + '\n')

