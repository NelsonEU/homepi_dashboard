import os
import secrets
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.api import system, minecraft  # you already have these

app = FastAPI()

# ---------- Basic Auth ----------

security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    """
    Simple HTTP Basic auth protecting the dashboard & APIs.
    Credentials come from env vars:
    - DASHBOARD_USER
    - DASHBOARD_PASSWORD
    """
    username = os.getenv("DASHBOARD_USER")
    password = os.getenv("DASHBOARD_PASSWORD")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Auth not configured on server",
        )

    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True


# ---------- API Routers (protected) ----------

app.include_router(system.router, dependencies=[Depends(basic_auth)])
app.include_router(minecraft.router, dependencies=[Depends(basic_auth)])

# ---------- Frontend (protected) ----------

BASE_DIR = Path(__file__).resolve().parent.parent  # ~/dashboard
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve index.html at "/"
@app.get("/", dependencies=[Depends(basic_auth)])
def dashboard_index():
    return FileResponse(FRONTEND_DIR / "index.html", media_type="text/html")

# app.mount(
#     "/static",
#     StaticFiles(directory=str(FRONTEND_DIR / "static")),
#     name="static",
# )
