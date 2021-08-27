from utils.path_manager import PathFinder
from utils.common import convert_to_auggy, get_image_info
import json
import os



"""Bounding Box Class"""
class BoundingBox:
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
    def __init__(self, ipath, fpath, width, height, depth):
        with open(fpath, 'r') as f: lines = f.readlines()
        self.image_name = os.path.basename(ipath)
        self.image_path = ipath
        self.path = fpath
        self.width = width
        self.height = height
        self.depth = depth
        self.bounding_box = []
        for line in lines:
            line = line.strip()
            data = line.split()
            label = int(data[0])
            bbox_width = float(data[3]) * width
            bbox_height = float(data[4]) * height
            center_x = float(data[1]) * width
            center_y = float(data[2]) * height
            xmin = int(center_x - (bbox_width / 2))
            ymin = int(center_y - (bbox_height / 2))
            xmax = int(center_x + (bbox_width / 2))
            ymax = int(center_y + (bbox_height / 2))
            self.bounding_box.append(BoundingBox(label, xmin, ymin, xmax, ymax))


"""
Decode classes.txt
"""
class YoloLabels:
    def __init__(self, cpath):
        with open(cpath, 'r') as f:
            labels = f.readlines()

        self.classes = {}
        for e, label in enumerate(labels):
            label = label.replace('\n', '')
            self.classes[e] = label

class OpenTextFile:
    def __init__(self):
        self.PF = PathFinder()

    def open(self, fpath):
        ipath, height, width, depth = self.get_image_info(fpath, self.PF.imageFolder, self.PF.imgFormat)
        txt = TextFile(ipath, fpath, width, height, depth)
        return convert_to_auggy(txt)




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

