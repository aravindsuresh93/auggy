from utils.path_manager import PathFinder
from utils.project_manager import ProjectManager
from analytics.label_stats import StatMaster
import falcon
import json
import os

print('init')

def decode(req):
    body = req.stream.read()
    body = body.decode('utf-8')
    if os.name =='nt':
        body = body.replace("\\", "\\\\")
    request = json.loads(body)
    return request


class Login:
    def on_post(self, req, resp):
        success = True
        message = "Feature yet to be implimented"
        data = {'success': success, 'message': message}
        resp.body = json.dumps(data)


class Projects:
    """
    Project Management
    """
    def on_get(self,req, resp):
        pm = ProjectManager()
        try:
            content,success, message = pm.get_projects()
        except Exception as e:
            content, success, message = {}, False, str(e)
        data = {'data': content, 'success': success, 'message': message}
        resp.body = json.dumps(data)

    def on_post(self, req, resp):
        pm = ProjectManager()
        request = decode(req)
        try:    
            method = request.get('method')
            if method == 'edit':
                success, message = pm.edit_project(request)
            elif method == 'create':
                success, message = pm.create_project(request)
            elif method == 'delete':
                success, message = pm.delete_project(request)
            elif method == 'current':
                success, message = pm.current(request)
            else:
                success, message = False, "Invalid Method"
        except Exception as e:
            success, message = False, str(e)
        resp.body = json.dumps({"success": success, "message": message})

class Upload:
    def on_get(self, req, resp):
        pass
    def on_post(self, req, resp):
        try:
            request = decode(req)
            source_image_folder = request.get('imageFolder','')
            assert len(source_image_folder), 'Image folder is empty'

            source_annotation_folder = request.get('annotationFolder','')
            assert len(source_annotation_folder), 'Annotation folder is empty'

            annotation_format = request.get('annotationFormat','')
            assert len(annotation_format), 'Annotation format is empty'
            PF = PathFinder()
            PF.__setattr__('annotationFormat', annotation_format)

            if annotation_format == 'txt':
                classes_path = request.get('classesPath','')
                assert len(classesPath), 'Classes path is empty'





class PathSet:

    def on_get(self, req, resp):
        try:
            PF = PathFinder()
            content = PF.__dict__
            success, message = True, ""
        except Exception as e:
            content, success, message = {}, False, str(e)
        data = {'data': content, 'success': success, 'message': message}
        resp.body = json.dumps(data)

    def on_post(self, req, resp):
        try:
            PF = PathFinder()
            request = decode(req)
            for k, v in request.items():
                PF.__setattr__(k, v)
            PF.save()
            success, message = True, ""
        except Exception as e:
            success, message = False, str(e)
        resp.body = json.dumps({"success": success, "message": message})



class PathSet_1:

    def on_get(self, req, resp):
        try:
            PF = PathFinder()
            content = PF.__dict__
            success, message = True, ""
        except Exception as e:
            content, success, message = {}, False, str(e)
        data = {'data': content, 'success': success, 'message': message}
        resp.body = json.dumps(data)

    def on_post(self, req, resp):
        try:
            PF = PathFinder()
            request = decode(req)
            for k, v in request.items():
                PF.__setattr__(k, v)
            PF.save()
            success, message = True, ""
        except Exception as e:
            success, message = False, str(e)
        resp.body = json.dumps({"success": success, "message": message})


class GetStats:
        
    def on_get(self, req, resp):
        try:
            self.PF = PathFinder()
            self.sm = StatMaster()
            image_info = self.sm.get_image_info()
            label_info = self.sm.get_label_info()
            bound_box_leak = self.sm.check_bounding_box_leak()
            content = {'imageInfo': image_info, 'labelInfo': label_info, 'boundBoxLeak' : bound_box_leak}
            success, message = True, ""
        except Exception as e:
            content, success, message = {}, False, str(e)

        data = {'data': content, 'success': success, 'message': message}
        resp.body = json.dumps(data)


class RenameLabel:

    def on_post(self, req, resp):
        try:
            self.PF = PathFinder()
            self.sm = StatMaster()
            request = decode(req)
            content = request.get('labels', [])
            success, message = self.sm.rename_label(content)
        except Exception as e:
            content, success, message = {}, False, str(e)
        resp.body = json.dumps({'success': success, 'message': message})

class DeleteLabel:

    def on_post(self, req, resp):
        self.PF = PathFinder()
        self.sm = StatMaster()
        # try:
        request = decode(req)
        content = request.get('labels', [])
        success, message = self.sm.delete_label(content)
        # except Exception as e:
        # content, success, message = {}, False, str(e)
        resp.body = json.dumps({'success': success, 'message': message})

class GetListOfImages:

    def on_post(self, req, resp):
        self.PF = PathFinder()
        self.sm = StatMaster()
        request = decode(req)
        class_name = request.get('class_name', [])
        try:
            content,success, message = self.sm.get_image_path_by_label(class_name)
        except Exception as e:
            content, success, message = [], False, str(e)

        data = {'data': content, 'success': success, 'message': message}
        resp.body = json.dumps(data)











app = falcon.API()
app.add_route('/login', Login())
app.add_route('/projects', Projects())
app.add_route('/paths', PathSet())
app.add_route('/stats', GetStats())
app.add_route('/rename', RenameLabel())
app.add_route('/delete', DeleteLabel())
app.add_route('/getimagebylabel', GetListOfImages())



print('ready')
# For windows
if os.name == 'nt':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8099) 


