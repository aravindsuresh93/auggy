import os
from posixpath import dirname
import xml.etree.cElementTree as ET

class SaveXML:
    @staticmethod
    def save(info, classes, save_folder):
        metainfo = info[0]
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "folder").text = os.path.dirname(metainfo['image_path'])
        ET.SubElement(annotation, "filename").text = os.path.basename(metainfo['image_path'])
        ET.SubElement(annotation, "path").text = metainfo['image_path']

        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "height").text = str(metainfo['height'])
        ET.SubElement(size, "width").text = str(metainfo['width'])
        ET.SubElement(size, "depth").text = str(metainfo['depth'])

        xml_name = os.path.basename(metainfo['annotation_path'])

        for b in info:
            object_element = ET.SubElement(annotation, "object")
            ET.SubElement(object_element, "name").text = classes.loc[b['label']].values[0]
            bndbox = ET.SubElement(object_element, "bndbox")
            for v in ['xmin', 'ymin', 'xmax', 'ymax']:
                ET.SubElement(bndbox, v).text = str(b[v])

        tree = ET.ElementTree(annotation)
        tree.write(os.path.join(save_folder, xml_name), encoding='utf-8', xml_declaration=True)







