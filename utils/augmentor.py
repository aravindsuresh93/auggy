import albumentations as A
from matplotlib import pyplot as plt
import random
import cv2
import os


class Augment:
    def __init__():
        self.bbox_params = A.BboxParams(format='pascal_voc')

    """
    Pixel Level
    """

    def blur(self, blur_limit):
        self.transform = A.Compose([A.Blur(blur_limit=(3, blur_limit), p=1)], bbox_params=self.bbox_params)

    def clahe(self, clip_limit):
        self.transform = A.Compose([A.CLAHE(clip_limit=clip_limit, tile_grid_size=(8, 8), p=1)], bbox_params=self.bbox_params)

    def ChannelDropout(self, channel_drop_range, fill_value):
        self.transform = A.Compose([A.ChannelDropout(channel_drop_range=channel_drop_range,fill_value= fill_value, p=1)], bbox_params=self.bbox_params)

    def ChannelShuffle(self):
        self.transform = A.Compose([A.ChannelShuffle(p=1)], bbox_params=self.bbox_params)

    def ChannelShuffle(self, brightness, contrast, saturation, hue):
        self.transform = A.Compose([A.ChannelShuffle(brightness=brightness, contrast=contrast,
                                                 saturation=saturation, hue=hue, p=1)], bbox_params=self.bbox_params)
    
    def Downscale(self, scale_min, scale_max):
        self.transform = A.Compose([A.Downscale(scale_min=scale_min, scale_max=scale_max p=1)], bbox_params=self.bbox_params)

    def Equalize(self, mode, by_channels):
        self.transform = A.Compose([A.Downscale(mode=mode, by_channels=by_channels p=1)], bbox_params=self.bbox_params)

    """
    Workflow
    """
    def response(transformed):
        boxes = []
        for e, box in enumerate(transformed["bboxes"]):
            box += transformed["category_ids"][e]
            boxes.append(box)
        image = transformed['image']
        return image, boxes

    def request(transform_data):
        self.transformation_type = transform_data.get("type", "")
        assert len(transformation_type), "Transformation type not available"

        self.transformation_parameters = transform_data.get("parameters", {})
        assert len(transformation_parameters), "Transformation parameters not available"

    def get_arg(argname, default_val):
        return self.transformation_parameters.get(argname, default_val)

    def process(self, image, boxes, transform_data):
        self.request(transform_data)

        """Blur"""
        if self.transformation_type == "blur":
            self.blur(blur_limit=self.get_arg("blur_limit", 3))

        """CLAHE"""
        if self.transformation_type == "clahe":
            self.clahe(self.get_arg("clip_limit", 4))

        """ChannelDropout"""
        if self.transformation_type == "ChannelDropout":fill_value
            self.ChannelDropout(self.get_arg("channel_drop_range", (1, 1)), self.get_arg("fill_value", 0))

        """ChannelShuffle"""
        if self.transformation_type == "ChannelShuffle":
            self.ChannelShuffle()

        """ColorJitter"""
        if self.transformation_type == "ColorJitter":
            self.ColorJitter(self.get_arg("brightness", 0.2), 
            self.get_arg("contrast", 0.2),
            self.get_arg("saturation", 0.2),
            self.get_arg("hue", 0.2))

        """Downscale"""
        if self.transformation_type == "Downscale":
            self.Downscale(self.get_arg("scale_min", 0.25), self.get_arg("scale_max", 0.25))

        """Equalize"""
        if self.transformation_type == "Equalize":
            self.Equalize(self.get_arg("mode", "cv"), self.get_arg("by_channels", True))


        transformed = self.transform(image=image, bboxes=boxes)
        return self.response(transformed)


"""
Blur - blur_limit (4-100)
CLAHE - clip_limit (1-100)
ChannelDropout - Randomly Drop Channels in the input Image. - channel_drop_range (1,2) , fill_value(0,255)
ChannelShuffle - Randomly rearrange channels of the input RGB image - no  params
ColorJitter - Randomly changes the brightness, contrast, and saturation of an image. brightness [0-1], contrast[0-1],saturation[0-1], hue[0-1]
Downscale - Decreases image quality by downscaling and upscaling back. - "scale_min" - [0-0.5], "scale_max" - [0-0.5]
Equalize - Equalize the image histogram. mode='cv'/'pil', by_channels=True
FDA
FancyPCA
FromFloat
GaussNoise
GaussianBlur
GlassBlur
HistogramMatching
HueSaturationValue
IAAAdditiveGaussianNoise
IAAEmboss
IAASharpen
IAASuperpixels
ISONoise
ImageCompression
InvertImg
MedianBlur
MotionBlur
MultiplicativeNoise
Normalize
Posterize
RGBShift
RandomBrightnessContrast
RandomFog
RandomGamma
RandomRain
RandomShadow
RandomSnow
RandomSunFlare
Sharpen
Solarize
ToFloat
ToGray
ToSepia
"""
