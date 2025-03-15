from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta,datetime
from typing import List
from database import get_session, create_db_and_tables
from models import User, UserCreate, UserRead, Project, ProjectCreate, ProjectRead, ProjectUpdate, Token
from auth import get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, get_admin_user

app = FastAPI(title="JWT Auth API with RBAC")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, role=user.role, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/projects", response_model=List[ProjectRead])
def get_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()

@app.post("/projects", response_model=ProjectRead, status_code=201)
def create_project(project: ProjectCreate,current_user: User = Depends(get_admin_user),session: Session = Depends(get_session)):
    db_project = Project.from_orm(project) 
    db_project.owner_id = current_user.id 
    session.add(db_project) 
    session.commit()  
    session.refresh(db_project)  
    return db_project

@app.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: int,project: ProjectUpdate,current_user: User = Depends(get_admin_user),session: Session = Depends(get_session)):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.dict(exclude_unset=True) 
    for key, value in project_data.items():
        setattr(db_project, key, value)

    db_project.updated_at = datetime.utcnow()  
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}", status_code=200)
def delete_project(project_id: int,current_user: User = Depends(get_admin_user),session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"detail": "Project deleted successfully"}