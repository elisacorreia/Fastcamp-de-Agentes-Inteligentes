from fastapi import FastAPI
from .task_manager import run

app = FastAPI()

@app.post("/run")
async def execute_run(payload: dict):
    return await run(payload)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)