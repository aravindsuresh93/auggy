import tornado.web
import tornado.ioloop
import os
import json

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
        

if (__name__ == "__main__"):
    app = tornado.web.Application([("/", upload_files),])
    app.listen(8088)
    tornado.ioloop.IOLoop.instance().start()
