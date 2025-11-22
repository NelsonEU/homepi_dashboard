from fastapi import FastAPI

from app.api import system, minecraft

app = FastAPI()


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Include domain routers
app.include_router(system.router)
app.include_router(minecraft.router)
