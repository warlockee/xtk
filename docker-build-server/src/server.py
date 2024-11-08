import os
import time
import threading
import subprocess
from queue import Queue
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
build_queue = Queue()
build_status: Dict[str, Dict[str, str]] = {}

class BuildRequest(BaseModel):
    user: str
    path: str
    tag: str

def build_docker_image(user: str, path: str, tag: str, build_id: str):
    build_status[build_id]['status'] = 'in-progress'
    try:
        # Build Docker image
        build_command = ["docker", "build", "-t", tag, path]
        result = subprocess.run(
            build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            build_status[build_id] = {
                "status": "failed",
                "log": f"Build failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            }
            return

        # Push the image to the registry
        push_command = ["docker", "push", tag]
        push_result = subprocess.run(
            push_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if push_result.returncode != 0:
            build_status[build_id] = {
                "status": "failed",
                "log": f"Push failed.\nSTDOUT:\n{push_result.stdout}\nSTDERR:\n{push_result.stderr}"
            }
            return

        # Build and push successful
        build_status[build_id] = {"status": "success", "log": "Build and push successful"}

    except Exception as e:
        build_status[build_id] = {"status": "failed", "log": str(e)}

    finally:
        build_queue.task_done()

def worker_thread():
    while True:
        user, path, tag, build_id = build_queue.get()
        build_docker_image(user, path, tag, build_id)

# Start the worker thread
threading.Thread(target=worker_thread, daemon=True).start()

@app.post("/build")
async def build(request: BuildRequest):
    user = request.user
    path = request.path
    tag = request.tag

    if not user or not path or not tag:
        raise HTTPException(status_code=400, detail="Missing required fields: 'user', 'path', 'tag'")

    if not os.path.exists(path):
        raise HTTPException(status_code=400, detail=f"Invalid path: {path} does not exist")

    # Generate a unique build ID for tracking
    build_id = f"{user}-{int(time.time())}"
    build_status[build_id] = {"status": "queued"}

    # Queue the build request
    build_queue.put((user, path, tag, build_id))

    return {"message": "Build queued", "build_id": build_id}

@app.get("/status/{build_id}")
async def status(build_id: str):
    status = build_status.get(build_id)
    if not status:
        raise HTTPException(status_code=404, detail="Invalid build ID")
    return status
