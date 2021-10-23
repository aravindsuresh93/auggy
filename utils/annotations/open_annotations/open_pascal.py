import xml.etree.ElementTree as ET
import xml
from utils.common import convert_to_auggy, get_image_info
import os

from clogger.clogger import CLogger
logger = CLogger.get("auggy-xml-file")


"""Bounding Box Class"""
class BoundingBoxXML:
    def __init__(self, master, classes):
        for child in master:
            if child.tag == 'name':
                if child.text not in classes.values():
                    classes[len(classes)] = child.text
                inverted_classes = {v:k for k,v in classes.items()}
                self.label = inverted_classes[child.text]
            if child.tag == 'bndbox':
                for grandchild in child:
                    if grandchild.tag in ['xmin', 'ymin', 'xmax', 'ymax']:
                        setattr(self, grandchild.tag, int(grandchild.text.strip()))
        self.h = self.ymax - self.ymin
        self.w = self.xmax - self.xmin


"""Converts XML into unified"""
class ParseXML:
    def __init__(self, fpath, image_folder, name, classes):
        try:
            root = ET.parse(fpath).getroot()
            self.annotation_path = fpath
            self.image_path, self.image_height, self.image_width, self.image_depth = get_image_info(image_folder, name)
            self.bounding_box = []
            for master in root:
                if master.tag == 'filename':
                    self.image_name = master.text

                """ %% Commenting out as image dimensions are captured from get_image_info
                if master.tag == 'size':
                    for child in master:
                        if child.tag in ['height', 'width', 'depth']:
                            setattr(self, f'image_{child.tag}', int(child.text.strip()))
                """

                if master.tag == 'object':
                    self.bounding_box.append(BoundingBoxXML(master, classes))

        except xml.etree.ElementTree.ParseError:
            self.error = f'{fpath} seems to be empty/ corrupted'
            self.annotation_path = fpath
            logger.error(self.error)
        except Exception as e:
            self.error = f'{fpath} {e}'
            self.annotation_path = fpath
            logger.error(self.error)


class OpenXMLFile:
    def open(self, fpath, image_folder, name, classes):
        xml = ParseXML(fpath, image_folder, name, classes)
        return convert_to_auggy(xml)
     


