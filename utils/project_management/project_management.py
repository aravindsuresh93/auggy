from utils.db_management.db_connector import DB
from fastapi import HTTPException
import json
import time


class ProjectManager:
    def __init__(self):
        self.db = DB()

    def create_project(self, request, username):
        metainfo = {'createdby': username, 'createdtime': int(time.time()), 'description': request.description}
        if not request.name:
            raise HTTPException(status_code=400, detail='project name is mandatory')
        data = (request.name, json.dumps(metainfo), json.dumps({}))
        status, message = self.db.create_project(data)
        if status: return status, message

        accesssdata = (username, request.name, "admin")
        s, m = self.db.insert_access(accesssdata)
        return status, message

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
        print(df)
        if not len(df):
            raise HTTPException(status_code=401, detail=f'{username} does not have permission to access {projectname}')
