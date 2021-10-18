from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from utils.user_management.authorization import AuthHandler
from utils.db_management.db_connector import DB
from utils.project_management.project_management import ProjectManager
from schemas.schemas import AuthDetails, Project
from typing import List

auth_handler = AuthHandler()
project_manager = ProjectManager()
app = FastAPI()
db = DB()

"""
Users
"""

@app.post('/user/register', status_code=201)
def register(auth_details: AuthDetails):
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    status, message = db.create_user(username=auth_details.username, password=hashed_password)
    return {"es": status, "message": message}

@app.post('/user/login')
def login(auth_details: AuthDetails):
    userinfo = db.get_user(auth_details.username)
    if not len(userinfo) or (not auth_handler.verify_password(auth_details.password, userinfo.get('password', '.'))):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(userinfo['username'])
    return {"access_token": token, "token_type": "bearer"}

@app.post('/user/edit')
def user_edit(username=Depends(auth_handler.auth_wrapper)):
    raise NotImplementedError

@app.post('/user/delete')
def user_delete(username=Depends(auth_handler.auth_wrapper)):
    raise NotImplementedError
    

"""
Projects
"""
@app.post('/project/create')
def project_create(req: Project, username=Depends(auth_handler.auth_wrapper)):
    status, message = project_manager.create(req, username)
    return {"es": status, "message": message}

@app.post('/project/delete')
def project_get_stats(req: Project, username=Depends(auth_handler.auth_wrapper)):
    print('delete req', username, req.projectname)
    project_manager.check_access(username, req.projectname)
    status, message = project_manager.delete(username, req.projectname)
    return {"es": status, "message": message}

@app.get('/project/list')
def project_list(username=Depends(auth_handler.auth_wrapper)):
    status, message, data = project_manager.list_projects(username)
    return {"es": status, "message": message, 'data': data}

"""
Stats
"""

@app.get('/{projectname}/getstats')
def get_stats(projectname, username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)

@app.post('/{projectname}/label/rename')
def rename_label(projectname, username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)

@app.post('/{projectname}/label/delete')
def delete_label(projectname, username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)

"""
fileupload
"""

@app.post("/{projectname}/upload/images")
async def create_upload_file(file: List[UploadFile] = File(...)):
    for f in file:
        print(f.filename)
    return {"yo": 'file.filename'}

@app.post("/{projectname}/upload/annotations")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/{projectname}/upload/artefacts")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

