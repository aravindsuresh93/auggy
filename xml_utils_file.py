import xml.etree.ElementTree as ET
import numpy as np

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
