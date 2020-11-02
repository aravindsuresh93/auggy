import shutil
import json
import os
from shutil import copyfile


project_config_file = 'project_config.json'

class ProjectManager:
    def __init__(self):
        self.load()

    def load(self):
        with open(project_config_file, 'r') as f:
                self.project_config = json.load(f)


    def current(self, request):
        self.load()
        projects, ret, msg = self.get_projects()
        if not ret:
            return ret, msg

        project_names = []
        project_ids = []
        for k,v in projects.items():
            project_names.append(v['name'])
            project_ids.append(k)

        name = request.get('name')
        setval = False
        for e, pn in enumerate(project_names):
            if name == pn:
                self.project_config['current'] = project_ids[e]
                self.save()
                setval = True
                break
        if not setval:
            return False, 'Project not found'
        return True, ''

    def get_projects(self):
        self.load()
        projects = self.project_config.get('projects', {})
        if not len(projects):
            return {}, True, 'No projects found'
        return projects, True, ''

    def edit_project(self,request):
        self.load()
        projects = self.project_config.get('projects', {})
        name = request.get('name', '')
        old_name = request.get('oldName', name)
        

        project_names = {}
        for k,v in projects.items():
            project_names[v['name']] = k

        if not old_name in project_names.keys():
            return False, 'Project name not found'

        project_id = project_names[old_name]
        description = request.get('description','')
        owner = request.get('owner','')
        projects[project_id] =  {"name": name,"description" : description, "owner" : owner}
        self.project_config['projects'] = projects
        self.save()
        return True, ''

    def create_project_structure(self, name):
        
        if not os.path.exists('data/'):
            os.makedirs('data/')
        os.makedirs(f'data/{name}')
        os.makedirs(f'data/{name}/original')
        os.makedirs(f'data/{name}/input_images')
        os.makedirs(f'data/{name}/input_annotations')  
        os.makedirs(f'data/{name}/output_images')
        os.makedirs(f'data/{name}/output_annotations')  
        self.set_initial_config(name)
        

    def set_initial_config(self,name):
        with open('templates/config.json', 'r') as f:
                template_config = json.load(f)
                
        template_config['imageFolder'] = f'data/{name}/input_images'
        template_config['annotationFolder'] = f'data/{name}/input_annotations'
        template_config['annotationFolder'] = f'data/{name}/classes.txt'

        with open(f'data/{name}/config.json', 'w') as f:
            json.dump(template_config, f)


    def create_project(self,request):
        self.load()
        projects = self.project_config.get('projects', {})
        name = request.get('name', '')
        assert len(name), 'Name is mandatory'
        
        project_names = []
        for k,v in projects.items():
            project_names.append(v['name'])

        if name in project_names:
            return False, 'Name already taken, please use another name'

        description = request.get('description','')
        owner = request.get('owner','')

        lastkey = max([int(val) for val in list(projects.keys())]) if len(projects)  else 0
        
        project_id = str(lastkey + 1)
        projects[project_id] = {"name": name,"description" : description, "owner" : owner}
        self.project_config['projects'] = projects
        self.create_project_structure(project_id)
        self.save()  
        return True, ''

    def delete_project(self, request):
        self.load()
        projects = self.project_config.get('projects', {})

        project_names = {}
        for k,v in projects.items():
            project_names[v['name']] = k

        name = request.get('name', '')
        if not name in project_names:
            return False, 'Project name not found'
        project_id = project_names[name]
        shutil.rmtree(f'data/{project_id}')
        projects.pop(project_id)
        self.project_config['projects'] = projects
        self.save()
        return True, ''

    def save(self):
        with open(project_config_file, 'w') as f:
            json.dump(self.project_config, f)