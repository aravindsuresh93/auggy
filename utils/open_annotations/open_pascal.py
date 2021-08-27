import xml.etree.ElementTree as ET
from utils.path_manager import PathFinder
from utils.common import convert_to_auggy, get, get_image_info
import numpy as np
import pandas as pd
import os



"""Bounding Box Class"""
class BoundingBoxXML:
    def __init__(self, master):
        for child in master:
            if child.tag == 'name':
                self.label = child.text
            if child.tag == 'bndbox':
                for grandchild in child:
                    if grandchild.tag in ['xmin', 'ymin', 'xmax', 'ymax']:
                        setattr(self, grandchild.tag, int(
                            grandchild.text.strip()))
        self.h = self.ymax - self.ymin
        self.w = self.xmax - self.xmin


"""Converts XML into unified"""
class ParseXML:
    def __init__(self, file):
        self.root = ET.parse(file).getroot()
        self.path = file
        self.image_path, self.height, self.width, self.depth = get_image_info(file)

        self.bbox = []
        for master in self.root:
            if master.tag == 'filename':
                self.image_name = master.text
            if master.tag == 'size':
                for child in master:
                    if child.tag in ['height', 'width', 'depth']:
                        setattr(self, child.tag, int(child.text.strip()))
            if master.tag == 'object':
                self.bbox.append(BoundingBoxXML(master))


class OpenXMLFile:
    def open(self, fpath):
        xml = ParseXML(fpath)
        return convert_to_auggy(xml)
     


def editXML(xpath, oldText, newText):
    root = ET.parse(xpath).getroot()
    for master in root:
        for child in master:
            if child.tag == 'name' and child.text == oldText:
                child.text = newText
    return root


def editXMLBatch(xmlPaths, oldText, newText):
    for xpath in xmlPaths:
        tree = ET.ElementTree(editXML(xpath, oldText, newText))
        tree.write(xpath, xml_declaration=True, encoding='utf-8')
    return 'Completed!'


def deleteAttribute(xpath, attr):
    root = ET.parse(xpath).getroot()
    dellist = []
    for master in root:
        if master.tag == 'object':
            for child in master:
                if child.tag == 'name' and child.text == attr:
                    dellist.append(master)
    for d in dellist:
        root.remove(d)
    return root


def DeleteXMLBatch(xmlPaths, attr):
    pos = 0
    for xpath in xmlPaths:
        tree = ET.ElementTree(deleteAttribute(xpath, attr))
        tree.write(xpath, xml_declaration=True, encoding='utf-8')
        pos = pos + 100/len(xmlPaths)
    return 'Completed!'
