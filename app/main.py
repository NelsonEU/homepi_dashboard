import os
import secrets
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from app.api import system, minecraft


app = FastAPI()

allowed_origins = os.getenv("DASHBOARD_ALLOWED_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Basic Auth ----------

security = HTTPBasic()

def basic_auth(request: Request,credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    if request.method == "OPTIONS":
        return True

    username = os.getenv("DASHBOARD_USER")
    password = os.getenv("DASHBOARD_PASSWORD")

    if not username or not password:
        raise HTTPException(status_code=500, detail="Auth not configured on server")

    correct_user = secrets.compare_digest(credentials.username, username)
    correct_pass = secrets.compare_digest(credentials.password, password)

    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True


# ---------- API Routers (protected) ----------

app.include_router(system.router, dependencies=[Depends(basic_auth)])
app.include_router(minecraft.router, dependencies=[Depends(basic_auth)])

# ---------- Frontend (protected) ----------

BASE_DIR = Path(__file__).resolve().parent.parent 
FRONTEND_BUILD_DIR = BASE_DIR / "public"          

@app.get("/", dependencies=[Depends(basic_auth)])
def dashboard_index():
    return FileResponse(FRONTEND_BUILD_DIR / "index.html")

@app.get("/{path:path}", dependencies=[Depends(basic_auth)])
def dashboard_static(path: str):
    file_path = FRONTEND_BUILD_DIR / path

    if file_path.is_file():
        return FileResponse(file_path)

    raise HTTPException(status_code=404)