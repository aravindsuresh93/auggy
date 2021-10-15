from fastapi import FastAPI, Depends, HTTPException
from utils.user_management.authorization import AuthHandler
from utils.db_management.db_connector import DB
from utils.project_management.project_management import ProjectManager
from schemas.schemas import AuthDetails, Project

auth_handler = AuthHandler()
project_manager = ProjectManager()
app = FastAPI()
db = DB()


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    status, message = db.create_user(username=auth_details.username, password=hashed_password)
    return {"es": status, "message": message}


@app.post('/login')
def login(auth_details: AuthDetails):
    userinfo = db.get_user(auth_details.username)
    if not len(userinfo) or (not auth_handler.verify_password(auth_details.password, userinfo.get('password', '.'))):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(userinfo['username'])
    return {"access_token": token, "token_type": "bearer"}


@app.post('/test')
def test(req: Test, username=Depends(auth_handler.auth_wrapper)):
    print(req.p1, req.p2, username)
    return {'name': req.p1, 'u': username}

@app.post('/project')
def project(req: Project, username=Depends(auth_handler.auth_wrapper)):
    project_manager.create(req, username)
