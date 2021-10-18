from utils.db_management.db_connector import DB
from fastapi import HTTPException
import json
import time
import os


class ProjectManager:
    def __init__(self):
        self.db = DB()

    @staticmethod
    def create_project_structure(name):
        BASE_FOLDER = "data_lake"
        if not os.path.exists(BASE_FOLDER):
            os.makedirs(BASE_FOLDER)
        os.makedirs(f'{BASE_FOLDER}/{name}')
        os.makedirs(f'{BASE_FOLDER}/{name}/input_images')
        os.makedirs(f'{BASE_FOLDER}/{name}/input_annotations')  
        os.makedirs(f'{BASE_FOLDER}/{name}/output_images')
        os.makedirs(f'{BASE_FOLDER}/{name}/output_annotations')  

    def create(self, request, username):
        metainfo = {'createdby': username, 'createdtime': int(time.time()), 'description': request.description}
        if not request.projectname:
            raise HTTPException(status_code=400, detail='project name is mandatory')
        data = (request.projectname, json.dumps(metainfo), json.dumps({}))
        status, message = self.db.create_project(data)
        if status: return status, message

        accesssdata = (username, request.projectname, "admin")
        s, m = self.db.insert_access(accesssdata)

        if not s and not status:
            ProjectManager.create_project_structure(request.projectname)
            
        return status, message

    def delete(self, username, projectname):
        try:
            status1, message1 = self.db.delete_access((username, projectname))
            status2, message2 = self.db.delete_project((projectname,))
            return status1 or status2, f"{message1} , {message2}"
        except Exception as e:
            print(e)
            return 1, e

    def list_projects(self, username):
        try:
            df = self.db.select(f"SELECT * FROM ACCESS WHERE username = '{username}'")
            if len(df):
                projects = df['projectname'].values
                projectfilter = str(tuple(projects)).replace(',', '') if len(projects) == 1 else str(tuple(projects))
                projectquery = f"SELECT * FROM PROJECTS WHERE projectname in {projectfilter}"
                projdf = self.db.select(projectquery)
                return 0, "", projdf.to_dict(orient='index')
            return 0, "No projects found", {}
        except Exception as e:
            print(e)
            return 1, e, {}

    def check_access(self, username, projectname):
        df = self.db.select(f"SELECT * FROM ACCESS where username = '{username}' and projectname = '{projectname}'")
        if not len(df):
            raise HTTPException(status_code=401, detail=f'{username} does not have permission to access {projectname}')
