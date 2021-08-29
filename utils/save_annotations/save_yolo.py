from utils.open_annotations.open_yolo import convert_to_yolo


import os

class SaveTXT:
    @staticmethod
    def convert_coordinates(size, box, classid):
        dw = 1.0/size[0]
        dh = 1.0/size[1]
        x = (box[0]+box[1])/2.0
        y = (box[2]+box[3])/2.0
        w = box[1]-box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y=y*dh
        h=h*dh
        return f'{classid} {x} {y} {w} {h}'

    @staticmethod       
    def save(info, classes, save_folder):
        yolo_text = ""
        for b in info:
            yololine = convert_to_yolo((b['width'], b['height']), (b['xmin'], b['xmax'], b['ymin'], b['ymax']), b['label'])
            yolo_text = yolo_text + yololine + "\n"
            txtfilename = os.path.basename(b['annotation_path'])

        with open(os.path.join(save_folder, txtfilename), 'w') as f:
            f.write(yolo_text)

    @staticmethod
    def save_classes(classes, save_folder):
        classes_txt = ""
        classes_array = classes[classes['deleted'] != False]['label'].values
        for c in classes_array:
            classes_txt = classes_txt + str(c) + "\n"
        with open(os.path.join(save_folder, "classes.txt"), 'w') as f:
            f.write(classes_txt)