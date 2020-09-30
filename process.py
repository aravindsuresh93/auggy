import xml.etree.ElementTree as ET
import pickle as pkl
import numpy as np
import random
import cv2
import os

from data_aug.bbox_util import *
from data_aug.data_aug import *


from utils.xml_utils import XMLEditor
from utils.txt_utils import EditTextFile

from augment_utils import randomTransform, transform_image
from utils.path_manager import PathFinder
PF = PathFinder()


def augment(ipath, annotation_path, outname, image_name, image_format, transform):

    img = cv2.imread(ipath)
    height, width, _ = img.shape

    if PF.annotationFormat == 'xml':
        XE = XMLEditor(annotation_path)
        bounding_box_list = XE.get_bounding_box()
        

        """Transform Boxes for randomTransform"""
        original_boxes, names = [], []
        for i, b in enumerate(bounding_box_list):
            bbox = np.array([b['xmin'], b['ymin'], b['xmax'], b['ymax'], i])
            original_boxes.append(bbox)
            names.append(b['name'])


        """Save Image"""
        transformed_img, newbboxes = transform_image(img, original_boxes, transform)
        new_height, new_width = transformed_img.shape[:2]


        """Save Image"""
        outim = outname + '.' +image_format
        cv2.imwrite(outim, transformed_img)

        """Save XML"""
        outxml = outname + '.xml'
        XE.edit(newbboxes, names, original_boxes,image_name, new_height, new_width)
        XE.save(outxml)
    

    else:
        ET = EditTextFile()
        original_boxes, names = ET.get_bounding_boxes(annotation_path)
        """Save Image"""
        transformed_img, newbboxes = transform_image(img, original_boxes, transform)
        new_height, new_width = transformed_img.shape[:2]

        """Save Image"""
        outim = outname + '.' +image_format
        cv2.imwrite(outim, transformed_img)

        """Save Text"""
        outtxt = outname + '.txt'
        ET.write(newbboxes, names, new_height, new_width, outtxt)



def main():
    files = os.listdir(PF.imageFolder)
    files_list = []
    formatlist = []
    for f in files:
        for fformat in PF.imgFormat:
            if f.split('.')[1] == fformat:
                files_list.append(f.split('.')[0])
                formatlist.append(fformat)

    FAILED_LIST = []
    for ef, f in enumerate(files_list):
        print(f, f'   [{ef+1}/{len(files_list)}]')

        ipath = os.path.join(PF.imageFolder, f) + '.' + formatlist[ef]
        annotation_path = os.path.join(PF.annotationFolder, f) + '.' +PF.annotationFormat

        n = random.randint(0, 3)

        transform_data = PF.transformationData.get("transform", {})
        assert len(transform_data), "Transromation data not available"

        for i, transform in enumerate(transform_data):

            transormation_type = transform.get("type", "")
            assert len(transform_data), "Transformation type not available"

            transformation_parameters = transform.get("parameters", {})
            assert len(transformation_parameters), "Transformation parameters not available"

            transformation_variation = int(transform.get("variation", 0))
            assert transformation_variation, "Number of transformation variations not available"

            for j in range(transformation_variation):
                dolist = [transormation_type]
                new_path = os.path.join(PF.augmentationOutputFolder, f"{f}_{transormation_type}_{str(j)}_{str(i)}")
                image_name = f"{f}_{transormation_type}_{str(j)}_{str(i)}.{formatlist[ef]}"

            # try:
                augment(ipath, annotation_path,new_path, image_name, formatlist[ef], transform)
            # except Exception as e:
            #     print('FAILED : ', e, annotation_path)
            #     FAILED_LIST.append(annotation_path)
            #     continue
        break

main()


