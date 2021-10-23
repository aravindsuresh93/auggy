from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.user_management.authorization import AuthHandler
from utils.db_management.db_connector import DB
from utils.project_management.project_management import ProjectManager
from utils.file_manager.file_manager import FileManager
from schemas.schemas import AuthDetails, Project
from typing import List


project_manager = ProjectManager()
auth_handler = AuthHandler()
app = FastAPI()
db = DB()

"""
CORS middleware
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    access_token, refresh_token = auth_handler.encode_token(userinfo['username'])
    return {"access_token": access_token, "refresh_token" : refresh_token,"token_type": "Bearer"}

@app.get('/user/refresh')
def project_create(username=Depends(auth_handler.auth_wrapper)):
    access_token, refresh_token = auth_handler.encode_token(username)
    return {"access_token": access_token, "refresh_token" : refresh_token,"token_type": "Bearer"}

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
fileupload
"""

@app.post("/{projectname}/upload/images")
async def upload_images(projectname, files: List[UploadFile] = File(...), username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)
    status, message = FileManager.upload_images(projectname, files)
    return {"es": status, "message": message}

@app.post("/{projectname}/upload/annotations")
async def upload_annotations(projectname, files: List[UploadFile]  = File(...), username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)
    status, message = FileManager.upload_annotations(projectname, files)
    return {"es": status, "message": message}

@app.post("/{projectname}/upload/artefacts")
async def upload_artefacts(projectname, files: List[UploadFile]  = File(...), username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)
    status, message = FileManager.upload_artefacts(projectname, files)
    return {"es": status, "message": message}

@app.post("/{projectname}/upload/build")
async def upload_build(projectname, username=Depends(auth_handler.auth_wrapper)):
    project_manager.check_access(username, projectname)
    status, message = FileManager.upload_build(projectname)
    return {"es": status, "message": message}


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


