import shutil
import json
import os

project_config_file = 'data/project_config.json'

class ProjectManager:
    def __init__(self):
        with open(project_config_file, 'r') as f:
                self.project_config = json.load(f)

    def get_projects(self):
        projects = self.project_config.get('projects', {})
        if not len(projects):
            return {}, True, 'No projects found'
        return projects, True, ''




    def edit_project(self,request):
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
        os.makedirs(f'data/{name}')
        os.makedirs(f'data/{name}/original')
        os.makedirs(f'data/{name}/input_images')
        os.makedirs(f'data/{name}/input_annotations')  
        os.makedirs(f'data/{name}/output_images')
        os.makedirs(f'data/{name}/output_annotations')  


    def new_project(self,request):
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
        project_id = str(len(projects) + 1)
        projects[project_id] = {"name": name,"description" : description, "owner" : owner}
        self.project_config['projects'] = projects
        self.create_project_structure(project_id)
        self.save()  
        return True, ''

    def delete_project(self, request):
        projects = self.project_config.get('projects', {})

        project_names = {}
        for k,v in projects.items():
            project_names[v['name']] = k

        if not old_name in project_names:
            return False, 'Project name not found'
            
        project_id = project_names[old_name]

        shutil.rmtree(f'data/{project_id}')
        projects.pop(project_id)
        self.project_config['projects'] = projects
        self.save()
        return True, ''




    def save(self):
        with open(project_config_file, 'w') as f:
            json.dump(self.project_config, f)