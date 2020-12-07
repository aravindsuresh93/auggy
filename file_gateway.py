import tornado.web
import tornado.ioloop
import os
import json
import zipfile
import time

from utils.path_manager import PathFinder

class Saver:
    def upload(self, files, filetype):
        self.PF = PathFinder()
        if filetype == 'images':
            fbasepath = self.PF.imageFolder
            self.save(files, fbasepath)
        elif filetype == 'annotations':
            fbasepath = self.PF.annotationFolder
            self.save(files, fbasepath)
        elif filetype == 'classes':
            for f in files:
                fh = open(f"{self.PF.classesPath}", "wb")
                fh.write(f.body)
                fh.close
        
    
    def save(self, files, fbasepath):
        for f in files:
            fname = os.path.basename(f.filename)
            fh = open(f"{fbasepath}/{fname}", "wb")
            fh.write(f.body)
            fh.close


class upload_files(tornado.web.RequestHandler):
    def post(self):
        try:
            saver = Saver()
            images = self.request.files.get("images")
            if images:
                saver.upload(images, 'images')
            
            annotations = self.request.files.get("annotations")
            if annotations:
                saver.upload(annotations, 'annotations')
            
            classes = self.request.files.get("classes")
            if classes:
                saver.upload(classes, 'classes')

            success = True
            message = ''
        except Exception as e:
            success = False
            message = str(e)

        self.write(json.dumps({'success' : success, 'message':message}))

    

class download_files(tornado.web.RequestHandler):

    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),os.path.relpath(os.path.join(root, file),os.path.join(path, '..')))

    def get_zip(dir_list):
        self.PF = PathFinder()
        base_dir = self.PF.baseDir
        self.file_name = f"{os.basename(base_dir)}_{int(time.time())}"
        zipf = zipfile.ZipFile(self.zip_name, 'w', zipfile.ZIP_DEFLATED)
        dir_list = [self.PF.outputFolder, self.PF.outputXMLFolder, self.PF.outputTXTFolder]
        for dir in dir_list:
            zipdir(dir, zipf)

        zipf.write(self.PF.classesPath)
        zipf.close()

    def grab_file(self)
        self.get_zip
        with open(self.file_name, 'r') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()

    def get(self):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_name)
        self.grab_file()
        
        

if (__name__ == "__main__"):
    app = tornado.web.Application([("/upload", upload_files),("/download", download_files)])
    app.listen(8088)
    tornado.ioloop.IOLoop.instance().start()
    
