import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import files, connections, graph

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(files.router)
app.include_router(connections.router)
app.include_router(graph.router)

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:1420", "tauri://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def first_message() :
    return {"status": "Psydian Cérebro Ativo"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")