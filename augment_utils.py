from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random
import cv2
import os

from data_aug.bbox_util import *
from data_aug.data_aug import *

from utils.path_manager import PathFinder

PF = PathFinder()

"""
Return Random Number
"""


def grn(low=0, high=255):
    return random.randint(low, high)


"""
Adjust gamma to change brightness
"""


def adjust_gamma(image, gamma=1.0):
    gamma = 0.1 if gamma == 0 else gamma
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) *255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


"""
randomly select a background to place roi
"""


def select_background():
    fpath = random.choice(os.listdir(PF.randombgdir))
    ipath = os.path.join(PF.randombgdir, fpath)
    img = cv2.imread(ipath)
    return img


"""
reshape and place roi on new background
"""


def get_background(fgshape, p=100):
    height = fgshape[0] + int(fgshape[0] * p / 100)
    width = fgshape[1] + int(fgshape[0] * p / 100)
    bg = select_background()

    height = max(500, height)
    width = max(500, width)

    bg = cv2.resize(bg, (height, width))
    return bg


"""
Generate Noise Map
"""


def noise(h=50, w=50):
    return np.random.randint(255, size=(h, w, 3))


"""
generate noise mask
"""


def noise_generator(img, rect_size=50, rand_rects=10):
    for i in range(grn(0, rand_rects)):
        height = img.shape[0]
        width = img.shape[1]

        x1 = grn(1, width - rect_size)
        y1 = grn(1, height - rect_size)

        nh = grn(10, rect_size)
        nw = grn(10, rect_size)

        noise_mask = noise(nh, nw)
        img[y1: y1 + nh, x1: x1 + nw] = noise_mask

    return img


def put_random_noise(fg, bboxes, padding=5):
    iboxes = []
    for bbox in bboxes:
        xmin = bbox[0]
        ymin = bbox[1]
        xmax = bbox[2]
        ymax = bbox[3]
        name = bbox[4]
        roi = fg[ymin:ymax, xmin:xmax]
        roi = noise_generator(roi)
        fg[ymin:ymax, xmin:xmax] = roi
        iboxes.append([xmin, ymin, xmax, ymax, name])

    return fg, iboxes


"""
Generate rectangles Canvas
"""

text_pool = """Python is a multi-paradigm programming language. 
Object-oriented programming and structured programming are fully supported, 
and many of its features support functional programming and aspect-oriented programming 
(including by metaprogramming[46] and metaobjects (magic methods)).[47] Many other paradigms are supported via extensions, 
including design by contract[48][49] and logic programming.[50]"""
texts = text_pool.split(' ')


def get_rectangular_canvas(height=500, width=500, nrect=50, ntext=10, padding=10):
    randcolor = [grn(0, 255), grn(0, 255), grn(0, 255)]
    canvas = np.ones((height, width, 3))
    for nz, z in enumerate(canvas):
        for ny, y in enumerate(z):
            canvas[nz][ny] = randcolor

    for _ in range(grn(1, nrect)):
        x1 = grn(1, width - padding)
        y1 = grn(1, height - padding)

        x2 = grn(x1, width - padding)
        y2 = grn(y1, height - padding)

        if y2 - y1 > 0 and x2 - x1 > 0:
            randcolor = (grn(0, 255), grn(0, 255), grn(0, 255))
            canvas = cv2.rectangle(
                canvas, (x1, y1), (x2, y2), randcolor, grn(1, 5))

    for _ in range(grn(1, ntext)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (grn(1, height - padding), grn(1, width - padding))
        fontScale = grn(1, 3)
        color = (grn(0, 255), grn(0, 255), grn(0, 255))
        thickness = grn(1, 3)
        canvas = cv2.putText(canvas, random.choice(
            texts), org, font, fontScale, color, thickness, cv2.LINE_AA)

    return canvas


"""
randomly select a background to place roi
"""


def select_rect_background():
    fpath = random.choice(os.listdir(PF.randomrectdir))
    ipath = os.path.join(PF.randomrectdir, fpath)
    img = cv2.imread(ipath)
    return img


"""
reshape and place roi on new background
"""


def get_rect_background(fgshape, p=100):
    height = fgshape[0] + int(fgshape[0] * p / 100)
    width = fgshape[1] + int(fgshape[0] * p / 100)
    bg = select_rect_background()

    height = max(1000, height)
    width = max(1000, width)

    bg = cv2.resize(bg, (height, width))
    return bg


"""
place roi randomly on a random rectanglesbackground
"""


# def random_place_rectangles(fg, bboxes, padding = 5):
#     height = fg.shape[0] + int(fg.shape[0] * 100/ 100)
#     width = fg.shape[1] + int(fg.shape[0] * 100/ 100)
#     bg = get_rectangular_canvas(height, width)

#     iboxes = []
#     for bbox in bboxes:
#         randx = random.randint(padding,bg.shape[1] - fg.shape[1] - padding)
#         randy = random.randint(padding,bg.shape[0] - fg.shape[0] - padding)
#         xmin = bbox[0]
#         ymin = bbox[1]
#         xmax = bbox[2]
#         ymax = bbox[3]
#         name = bbox[4]
#         roi = fg[ymin:ymax, xmin:xmax]
#         bg[randy : randy + roi.shape[0], randx : randx + roi.shape[1]] = roi
#         iboxes.append([randx, randy, xmax - xmin + randx, ymax - ymin + randy, name])

#     return bg, iboxes

def random_place_rectangles(fg, bboxes, padding=5):
    bg = get_rect_background(fg.shape)
    iboxes = []
    for bbox in bboxes:
        randx = random.randint(padding, bg.shape[1] - fg.shape[1] - padding)
        randy = random.randint(padding, bg.shape[0] - fg.shape[0] - padding)
        xmin = bbox[0]
        ymin = bbox[1]
        xmax = bbox[2]
        ymax = bbox[3]
        name = bbox[4]

        roi = fg[ymin:ymax, xmin:xmax]
        bg[randy: randy + roi.shape[0], randx: randx + roi.shape[1]] = roi
        iboxes.append([randx, randy, xmax - xmin +
                       randx, ymax - ymin + randy, name])
    return bg, iboxes


"""
place roi randomly on a random background
"""


def random_place(fg, bboxes, padding=5):
    bg = get_background(fg.shape)
    iboxes = []
    for bbox in bboxes:
        randx = random.randint(padding, bg.shape[1] - fg.shape[1] - padding)
        randy = random.randint(padding, bg.shape[0] - fg.shape[0] - padding)

        xmin = bbox[0]
        ymin = bbox[1]
        xmax = bbox[2]
        ymax = bbox[3]
        name = bbox[4]

        roi = fg[ymin:ymax, xmin:xmax]

        bg[randy: randy + roi.shape[0], randx: randx + roi.shape[1]] = roi

        iboxes.append([randx, randy, xmax - xmin +
                       randx, ymax - ymin + randy, name])

    return bg, iboxes


"""
convert to B&W
"""


def random_gray(img, minimum_gamma,maximum_gamma):
    minimum_gamma,maximum_gamma =  minimum_gamma * 100 ,maximum_gamma*100
    img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    img = adjust_gamma(img, gamma=float(random.randint(20, 100) / 100))
    return img


"""
randomly scale
"""

def calculate_scale(minval=1, maxval=4, div=100):
    minval = minval * 100
    maxval = maxval * 100
    fx = random.randint(minval, maxval) / div
    fy = random.randint(minval, maxval) / div
    return fx, fy

def randomScale(img, bboxes, fx,fy):
    retBoxes = []
    img = cv2.resize(img, None, fx=fx, fy=fy)
    for e, bbox in enumerate(bboxes):
        xmin, ymin, xmax, ymax,name = bbox[0], bbox[1], bbox[2], bbox[3], bbox[4]
        xmin, xmax, ymin, ymax = int(fx * xmin), int(fx * xmax), int(fy * ymin), int(fy * ymax)
        bbox = [xmin, ymin, xmax, ymax, name]
        retBoxes.append(bbox)
    return img, retBoxes

def adjust_contrast(image, gamma):
    image = Image.fromarray(image)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(gamma)
    image = np.asarray(image)
    return image

def adjust_sharpness(image, gamma):
    image = Image.fromarray(image)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(gamma)
    image = np.asarray(image)
    return image

def adjust_sauration(image, gamma):
    image = Image.fromarray(image)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(gamma)
    image = np.asarray(image)
    return image

def adjust_blur(image, gamma):
    image = Image.fromarray(image)
    image = image.filter(ImageFilter.GaussianBlur(gamma))
    image = np.asarray(image)
    return image

def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH)), nH, nW


import time
def horizontal_rotate(image, bboxes, angle):
    boxes = []
    if angle == -90:
        img,nH, nW = rotate_bound(image, -90)
    
        for box in bboxes:
            xmin, ymin, xmax, ymax,name= box
            nymin = nH - xmax
            nxmin = ymin
            nxmax = ymax
            nymax = nH - xmin
            boxes.append([nxmin, nymin, nxmax, nymax,name])
    
    if angle == 90:
        img,nH, nW = rotate_bound(image, 90)
    
        for box in bboxes:
            xmin, ymin, xmax, ymax,name= box
            nymin = xmin
            nxmin = nW - ymax
            nxmax = nW - ymin
            nymax = xmax
            boxes.append([nxmin, nymin, nxmax, nymax,name])
    return img, boxes
    




"""
Do various transformations
"""


def randomTransform(img, bboxes, dolist=[]):
    bboxes = np.array(bboxes)

    if 'RandomScale' in dolist:
        img, bboxes = randomScale(img.copy(), bboxes.copy())
    if 'RandomTranslate' in dolist:
        img, bboxes = RandomTranslate(float(random.randint(0, 10) / 100), diff=True)(img.copy(), bboxes.copy())
    if 'RandomRotate' in dolist:
        img, bboxes = RandomRotate(random.randint(-360, 360))(img.copy(), bboxes.copy())
    if 'RandomShear' in dolist:
        img, bboxes = RandomShear(float(random.randint(-40, 40) / 100))(img.copy(), bboxes.copy())  # default -10,10
    if 'Resize' in dolist:
        img, bboxes = Resize(500)(img.copy(), bboxes.copy())
    if 'brightness' in dolist:
        img = adjust_gamma(img, gamma=float(random.randint(20, 100) / 100))
    if 'randomgray' in dolist:
        img = random_gray(img.copy())
    if 'randomplace' in dolist:
        img, bboxes = random_place(img.copy(), bboxes.copy())
    if 'randomplacerectangles' in dolist:
        img, bboxes = random_place_rectangles(img.copy(), bboxes.copy())
    if 'randomnoise' in dolist:
        img, bboxes = put_random_noise(img.copy(), bboxes.copy())

    return img, bboxes


def transform_image(img, bboxes, transform):
    bboxes = np.array(bboxes)

    transformation_type = transform.get("type", "")
    assert len(transformation_type), "Transformation type not available"

    transformation_parameters = transform.get("parameters", {})
    assert len(transformation_parameters), "Transformation parameters not available"

    transformation_variation = int(transform.get("variation", 0))
    assert transformation_variation, "Number of transformation variations not available"

    """
    1. Shape Transformations
    """

    """Scale Transformation"""
    if transformation_type == 'scale':
        transformation_method = transformation_parameters.get("method", "")
        assert len(transformation_method), "Transformation method not available"

        maximum_factor = transformation_parameters.get("maximum_factor", 2)
        minimum_factor = transformation_parameters.get("minimum_factor", 2)

        if transformation_method == 'up':
            fx, fy  = calculate_scale(maxval = maximum_factor, div = 100)
        elif transformation_method == 'down':
            fx, fy = calculate_scale(minval = minimum_factor, div = 1000)
        else:
            fx, fy = calculate_scale(minval = minimum_factor,maxval = maximum_factor, div = 1000)
        img, bboxes = randomScale(img.copy(), bboxes.copy(), fx, fy)
    
    """Rotate Transformation"""
    if transformation_type == 'rotate':
        minium_angle = transformation_parameters.get("miniumAngle", -90)
        maximum_angle = transformation_parameters.get("maximumAngle", 90)
        print(minium_angle, maximum_angle)
        img, bboxes = RandomRotate(random.randint(minium_angle, maximum_angle))(img.copy(), bboxes.copy())

    """Horizontal Rotate Transformation"""
    if transformation_type == 'horizontalRotate':
        transformation_method = transformation_parameters.get("method", "")
        assert len(transformation_method), "Transformation method not available"

        if transformation_method == 'left':
            rotate_angle = -90
        elif transformation_method == 'right':
            rotate_angle = 90
        else:
            rotate_angle = random.choice([-90,90])
        img, bboxes = horizontal_rotate(img.copy(), bboxes.copy(), rotate_angle)
    
    """Vertical Flip Transformation"""
    if transformation_type == 'verticalFlip':
        rotate_angle = 180
        img, bboxes = RandomRotate(rotate_angle)(img.copy(), bboxes.copy())

    """Vertical Flip Transformation"""
    if transformation_type == 'horizontalFlip':    
        img, bboxes = HorizontalFlip()(img.copy(), bboxes.copy())

    """Random Shear"""
    if transformation_type == 'randomShear':    
        minium_angle = transformation_parameters.get("miniumAngle", -90)
        maximum_angle = transformation_parameters.get("maximumAngle", 90)
        img, bboxes = RandomShear(float(random.randint(minium_angle, maximum_angle) / 100))(img.copy(), bboxes.copy()) 

    """Resize Box"""
    if transformation_type == 'resize':  
        inputDimension = transformation_parameters.get("inputDimension", 0)
        assert inputDimension, f"Invalid dimension : {inputDimension}"

    """Resize Particular Shape"""

    #Pending


    """
    1. Color Transformations
    """

    """Random Greyscale"""
    if transformation_type == 'randomgray':
        minium_gamma = int(transformation_parameters.get("miniumGamma", 0))
        maximum_gamma = int(transformation_parameters.get("maximumGamma", 2))
        img = random_gray(img.copy(), minium_gamma, maximum_gamma)

    """brightness"""
    if transformation_type == "brightness":
        minium_gamma = int(transformation_parameters.get("miniumGamma", 0))
        maximum_gamma = int(transformation_parameters.get("maximumGamma", 2))
        img = adjust_gamma(img, gamma=float(random.randint(minium_gamma * 100, maximum_gamma * 100) / 100))

    """contrast"""
    if transformation_type == "contrast":
        minium_gamma = int(transformation_parameters.get("miniumGamma", 0))
        maximum_gamma = int(transformation_parameters.get("maximumGamma", 2))
        img = adjust_contrast(img, gamma=float(random.randint(minium_gamma * 100, maximum_gamma * 100) / 100))

    """sharpness"""
    if transformation_type == "sharpness":
        minium_gamma = int(transformation_parameters.get("miniumGamma", 0))
        maximum_gamma = int(transformation_parameters.get("maximumGamma", 2))
        img = adjust_sharpness(img, gamma=float(random.randint(minium_gamma * 100, maximum_gamma * 100) / 100))
    

    """saturation"""
    if transformation_type == "saturation":
        minium_gamma = int(transformation_parameters.get("miniumGamma", 0))
        maximum_gamma = int(transformation_parameters.get("maximumGamma", 2))
        img = adjust_sauration(img, gamma=float(random.randint(minium_gamma * 100, maximum_gamma * 100) / 100))
    
    """blur"""
    if transformation_type == "blur":
        minium_gamma = int(transformation_parameters.get("miniumGamma", 0))
        maximum_gamma = int(transformation_parameters.get("maximumGamma", 5))
        img = adjust_blur(img, gamma=float(random.randint(minium_gamma * 100, maximum_gamma * 100) / 100))


    return img, bboxes
