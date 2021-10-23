from utils.common import convert_to_auggy, get_image_info
import os

from clogger.clogger import CLogger
logger = CLogger.get("auggy-text-file")



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

"""Converts TXT into unified object"""
class TextFile:
    def __init__(self, ipath, fpath, width, height, depth):
        try:
            with open(fpath, 'r') as f: lines = f.readlines()
            self.image_name = os.path.basename(ipath)
            self.image_path = ipath
            self.annotation_path = fpath
            self.image_width = width
            self.image_height = height
            self.image_depth = depth
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
        except Exception as e:
            self.error = f'{fpath} {e}' 
            self.annotation_path = fpath
            logger.error(self.error)



class OpenTextFile:
    def open(self, fpath, image_folder, name, classes = {}):
        ipath, height, width, depth = get_image_info(image_folder, name)
        txt = TextFile(ipath, fpath, width, height, depth)
        return convert_to_auggy(txt)


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



