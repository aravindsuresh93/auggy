import pandas as pd
import os

from utils.path_manager import PathFinder
from utils.xml_utils import editXMLBatch, flattenXML,DeleteXMLBatch
from utils.txt_utils import TxtExtract, EditClasses, DeleteClass

PF = PathFinder()

"""XML UTILS"""

metadata = ['path', 'image_name', 'image_path', 'width', 'height', 'depth']


class StatMaster:
    def __init__(self):
        self.annotation_files = []
        self.annotation_info = {}
        self.df = []
        self.attributes = pd.DataFrame()
        self.loader()

    def getMetaDF(self, baseDir, annotation_format='xml'):
        annotation_format = '.' + annotation_format
        data = []
        self.annotation_info = {}
        self.annotation_files = [file for file in os.listdir(baseDir) if annotation_format in file]


        if annotation_format == '.xml':
            for file in self.annotation_files:
                masterdict, info = flattenXML(os.path.join(baseDir, file))
                data.append(masterdict)
                self.annotation_info[file] = info


        if annotation_format == '.txt':
            TE = TxtExtract()
            for file in self.annotation_files:
                if file == 'classes.txt':
                    continue
                masterdict, info = TE.extract(os.path.join(baseDir, file))
                data.append(masterdict)
                self.annotation_info[file] = info

        self.df = pd.DataFrame(data)

    def loader(self):
        print('Loader')
        PF.load()
        self.getMetaDF(PF.annotationFolder, PF.annotationFormat)
        self.attributes = self.df.drop(metadata, 1)
        self.attrCount = {}
        for att in self.attributes.columns:
            self.attrCount.update({att: int(self.attributes[att].sum())})

    def filterPath(self, attribute):
        return self.df[self.df[attribute].notnull()]['path'].values

    def get_image_path_by_label(self, attribute):
        if attribute not in self.df.columns:
            return [], False, 'Label not found'
        image_paths = self.df[self.df[attribute].notnull()]['image_path'].values
        image_names = []
        for i in image_paths.tolist():
            image_names.append(os.path.basename(i))
        return image_names, True, ''

    def get_label_distribution(self):
        return self.attrCount

    def get_number_of_labels(self):
        return len(self.attrCount)

    def get_label_info(self):
        labels = self.get_label_distribution()
        label_count = self.get_number_of_labels()
        return {'total': label_count, 'labels': labels}

    def get_total_annotations(self):
        total_annotations = 0
        for k, v in self.attrCount.items():
            total_annotations += v
        return total_annotations

    def get_total_images(self):
        return len(self.df)

    def get_image_info(self):
        self.loader()
        total_images = self.get_total_images()
        total_annotations = self.get_total_annotations()
        nullannotations = self.get_null_annotations()
        missing = self.get_missing_annotations()
        return {'images': total_images, 'annotations': total_annotations, 'noAnnotationFile': missing,
                'nullAnnotations': nullannotations}

    def get_null_annotations(self):
        labeldf = self.df.drop(metadata, 1)
        cols = labeldf.columns
        null_annotations = []
        for idx, row in labeldf.iterrows():
            if row.isnull().sum() == len(cols):
                null_annotations.append(self.df.loc[idx]['image_path'])

        return {'total': len(null_annotations), 'images': null_annotations}

    def get_missing_annotations(self):
        files = os.listdir(PF.imageFolder)
        missing_annotations = []
        for file in files:
            ff_flag = 0
            for fformat in PF.imgFormat:
                if fformat in file:
                    ff_flag = 1
                    break
            if not ff_flag:
                continue

            imname = file.split('.' + fformat)[0]
            annotation_filename = imname + '.' + PF.annotationFormat
            if annotation_filename not in files:
                missing_annotations.append(file)
        return {'total': len(missing_annotations), 'images': missing_annotations}

    def rename_label(self, content):
        notfound = []
        for c in content:
            oldname = c.get('oldName', '')
            if oldname not in self.attrCount.keys():
                notfound.append(oldname)

        if len(notfound):
            return False, f"Labels {notfound} not found, please check the spelling."

        EC = EditClasses()
        for c in content:
            oldname = c.get('oldName', '')
            newname = c.get('newName', '')
            if PF.annotationFormat == 'xml':
                att_paths_ = self.filterPath(oldname)
                editXMLBatch(att_paths_, oldname, newname)
            elif PF.annotationFormat == 'txt':
                EC.rename(oldname,newname)

            self.loader()
        return True, ""

    def delete_label(self, content):
        notfound = []
        for c in content:
            oldname = c.get('oldName', '')
            if oldname not in self.attrCount.keys():
                notfound.append(oldname)

        if len(notfound):
            return False, f"Labels {notfound} not found, please check the spelling."

        if PF.annotationFormat == 'xml':
            for c in content:
                oldname = c.get('oldName', '')
                att_paths_ = self.filterPath(oldname)
                DeleteXMLBatch(att_paths_, oldname)

        if PF.annotationFormat == 'txt':

            # return False, "Implementation in progress"
            DC = DeleteClass()
            tbdel = []
            for c in content:
                oldname = c.get('oldName', '')
                if len(oldname):
                    tbdel.append(oldname)

            DC.delete(tbdel)
            self.loader()
        return True, ""

    def check_bounding_box_leak(self):
        LeakedXMLs = []
        for file, xml in self.annotation_info.items():
            leak = {}
            height = xml.height
            width = xml.width
            leakedbox = []
            for att in xml.bbox:
                name = att.label
                xmin = att.xmin
                ymin = att.ymin
                xmax = att.xmax
                ymax = att.ymax

                if xmin < 0 or ymin < 0 or xmax < 0 or ymax < 0 or xmin > width or ymin > height or xmax > width or ymax > height:
                    leakedbox.append(name)
                    leakedbox.append({'width': width, 'height': height})
                    leakedbox.append({'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})

            if len(leakedbox):
                leak.update({file: leakedbox})
            if len(leak):
                LeakedXMLs.append(leak)

        if len(LeakedXMLs):
            return {'total': len(leakedbox), 'images': LeakedXMLs}
        return {'total': 0, 'images': []}
