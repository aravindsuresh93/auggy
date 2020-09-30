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

class Projects:
    def on_get(self,req, resp):
        pm = ProjectManager()
        # try:
        content,success, message = pm.get_projects()
        # except Exception as e:
        #     content, success, message = {}, False, str(e)
        data = {'data': content, 'success': success, 'message': message}
        resp.body = json.dumps(data)


    def on_post(self, req, resp):
        pm = ProjectManager()
        request = decode(req)
        try:
            method = request.get('method')
            if method == 'edit':
                success, message = pm.edit_project(request)
            elif method == 'new':
                success, message = pm.new_project(request)
            elif method == 'delete':
                success, message = pm.delete_project(request)
        except Exception as e:
            success, message = False, str(e)
        resp.body = json.dumps({"success": success, "message": message})





app = falcon.API()
app.add_route('/paths', PathSet())
app.add_route('/stats', GetStats())
app.add_route('/rename', RenameLabel())
app.add_route('/delete', DeleteLabel())
app.add_route('/getimagebylabel', GetListOfImages())
app.add_route('/projects', Projects())


print('ready')
# For windows
if os.name == 'nt':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8099) 


