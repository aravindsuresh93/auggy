import xml.etree.ElementTree as ET
from utils.path_manager import PathFinder
from utils.common import convert_to_auggy
import numpy as np
import pandas as pd
import os


"""
Edit XML after augmentation and return root
"""


class XMLEditor:
    def __init__(self, xpath):
        self.root = ET.parse(xpath).getroot()

    def edit_meta(self, filename, height, width):
        for tag in self.root.findall('filename'):
            tag.text = filename

        for master in self.root:
            if master.tag == 'size':
                for child in master:
                    if child.tag == 'height':
                        child.text = str(height)
                    if child.tag == 'width':
                        child.text = str(width)

    def edit_single_box(self, xmin, ymin, xmax, ymax, original_bbox, label):
        for tag in self.root.findall('object'):
            upd = False
            for subtag in tag:
                if subtag.tag == 'name':
                    if subtag.text == label:
                        upd = True
                if subtag.tag == 'bndbox' and upd == True:
                    editFlag = 0
                    for s in subtag:
                        if s.tag == 'xmin' and int(s.text) == int(original_bbox[0]):
                            editFlag += 1
                        if s.tag == 'ymin' and int(s.text) == int(original_bbox[1]):
                            editFlag += 1
                        if s.tag == 'xmax' and int(s.text) == int(original_bbox[2]):
                            editFlag += 1
                        if s.tag == 'ymax' and int(s.text) == int(original_bbox[3]):
                            editFlag += 1

                    if editFlag == 4:
                        for s in subtag:
                            if s.tag == 'xmin' and int(s.text) == int(original_bbox[0]):
                                s.text = str(xmin)
                            if s.tag == 'ymin' and int(s.text) == int(original_bbox[1]):
                                s.text = str(ymin)
                            if s.tag == 'xmax' and int(s.text) == int(original_bbox[2]):
                                s.text = str(xmax)
                            if s.tag == 'ymax' and int(s.text) == int(original_bbox[3]):
                                s.text = str(ymax)

    def edit_boxes(self, original_bbox, bboxes, names, height, width):
        for i, bbox in enumerate(bboxes):
            ob = original_bbox[i]
            xmin, ymin, xmax, ymax = bbox[0], bbox[1], bbox[2], bbox[3]
            xmin = 1 if xmin <= 0 else xmin
            ymin = 1 if ymin <= 0 else ymin
            xmax = 1 if xmax <= 0 else xmax
            ymax = 1 if ymax <= 0 else ymax

            ymax = height - 1 if (ymax >= height) else ymax
            xmax = width - 1 if (xmax >= width) else xmax
            label = names[bbox[4]]

            self.edit_single_box(xmin, ymin, xmax, ymax, ob, label)

    def edit(self, bboxes, names, original_bbox, filename, height, width):
        self.edit_meta(filename, height, width)
        self.edit_boxes(original_bbox, bboxes, names, height, width)

    def save(self, outxml):
        tree = ET.ElementTree(self.root)
        tree.write(outxml, xml_declaration=True, encoding='utf-8')

    def get_bounding_box(self):
        boundlist = []
        for tag in self.root.findall('object'):
            bound = {}
            for subtag in tag:
                if subtag.tag == 'name':
                    bound.update({subtag.tag: subtag.text})

                if subtag.tag == 'bndbox':
                    for s in subtag:
                        bound.update({s.tag: int(s.text)})
            boundlist.append(bound)
        return boundlist


def get_corr_image(fpath):
    PF = PathFinder()
    name = os.path.basename(fpath)
    name = name.split('.xml')[0]
    images = os.listdir(PF.imageFolder)
    found = 0
    for fformat in PF.imgFormat:
        image_name = f'{name}.{fformat}'
        if image_name in images:
            found = 1
            break
    if found:
        ipath = os.path.join(PF.imageFolder, image_name)
        return ipath
    return ''


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
        self.image_path = get_corr_image(file)
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


def flattenXML(file):
    masterDict = {}
    xml = ParseXML(file)
    masterDict.update(  {'path': xml.path, 'image_name': xml.image_name,
                        'image_path': xml.image_path, 'height': xml.height,
                        'width': xml.width, 'depth': xml.depth})

    for att in xml.bbox:
        attval = masterDict.get(att.label, 0)
        attval += 1
        masterDict.update({att.label: attval})
    return masterDict, xml


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
