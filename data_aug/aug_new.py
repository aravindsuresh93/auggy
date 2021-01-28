import random

import cv2
from matplotlib import pyplot as plt

import albumentations as A

BOX_COLOR = (255, 0, 0) # Red
TEXT_COLOR = (255, 255, 255) # White


def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image"""
    x_min, y_min, x_max, y_max = bbox

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35, 
        color=TEXT_COLOR, 
        lineType=cv2.LINE_AA,
    )
    return img


def visualize(image, bboxes, category_ids, category_id_to_name):
    img = image.copy()
    for bbox, category_id in zip(bboxes, category_ids):
        class_name = category_id_to_name[category_id]
        img = visualize_bbox(img, bbox, class_name)
    cv2.imwrite("out.jpg", img)


cpath = r"C:\Users\ds\Desktop\Projects\test_images\yolo\classes.txt"
ipath = r"C:\Users\ds\Desktop\Projects\test_images\yolo\JIY4434.jpg"
tpath = r"C:\Users\ds\Desktop\Projects\test_images\yolo\JIY4434.txt"



def load_classes(cpath):
    with open(cpath, 'r') as f:
        labels = f.readlines()

    classes = {}
    for e, label in enumerate(labels):
        label = label.replace('\n', '')
        classes[str(e)] = label
    return classes

classes = load_classes(cpath)


def open_txt(classes, tpath,width, height):
    with open(tpath, "r") as f:
        lines = f.readlines()

    labels = []
    boxes = []

    for line in lines:
        line = line.strip()
        data = line.split()
        label = data[0]
        x_center = float(data[1])
        y_center = float(data[2] )
        width = float(data[3] )
        height = float(data[4])
        boxes.append([x_center, y_center, width, height])
        labels.append(label)
    return boxes, labels

image = cv2.imread(ipath)
height, width = image.shape[:2]
boxes, labels = open_txt(classes, tpath, width, height)



transform = A.Compose(
    [ A.ShiftScaleRotate(p=0.5)],
    bbox_params=A.BboxParams(format='yolo', label_fields=['category_ids']),
)



random.seed(7)
transformed = transform(image=image, bboxes=boxes, category_ids=labels)

new_boxes = []


print(height, width)
for data in transformed["bboxes"]:
    print(data)

    bbox_width = float(data[2]) * width
    bbox_height = float(data[3]) * height
    center_x = float(data[0]) * width
    center_y = float(data[1]) * height

    print("centre",center_x, center_y)

    xmin = int(center_x - (bbox_width / 2))
    ymin = int(center_y - (bbox_height / 2))
    xmax = int(center_x + (bbox_width / 2))
    ymax = int(center_y + (bbox_height / 2))

    new_boxes.append([xmin, ymin, xmax, ymax])
    
print(new_boxes)
visualize(
    transformed['image'],
    new_boxes,
    transformed['category_ids'],
    classes,
)

