import os
import tempfile
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import docker

app = FastAPI(title="Tooliyahub API")

# Docker engine se connect karna
try:
    docker_client = docker.from_env()
except Exception as e:
    print(f"Docker connect error: {e}")

@app.get("/")
async def read_root():
    return {"status": "Tooliyahub Backend Engine is Live!"}

@app.websocket("/ws/run")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("\x1b[1;32mTooliyahub Terminal Connected...\x1b[0m\r\n")
    
    running_container = None
    temp_script_path = None

    try:
        while True:
            # Browser se code receive karna
            code = await websocket.receive_text()
            await websocket.send_text("\x1b[1;33mExecuting your code in secure sandbox...\x1b[0m\r\n")
            
            # Code ko ek temporary python file me save karna
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as temp_file:
                temp_file.write(code)
                temp_script_path = temp_file.name

            try:
                # Naya isolated container start karna (Abhi testing ke liye default python image)
                running_container = docker_client.containers.run(
                    "python:3.10-slim", 
                    f"python /tmp/{os.path.basename(temp_script_path)}",
                    volumes={os.path.dirname(temp_script_path): {'bind': '/tmp', 'mode': 'ro'}},
                    detach=True,
                    mem_limit="100m", # Maximum 100MB RAM user limit
                    nano_cpus=500000000 # Maximum 0.5 CPU limit
                )
                
                # Live terminal output stream karna
                for line in running_container.logs(stream=True):
                    await websocket.send_text(line.decode('utf-8').replace('\n', '\r\n'))
                    
                # Code poora run hone ke baad container delete kar dena
                running_container.remove(force=True)
                running_container = None
                
            except Exception as e:
                await websocket.send_text(f"\x1b[1;31mExecution Error:\x1b[0m {str(e)}\r\n")
            finally:
                # Temporary file delete karna
                if temp_script_path and os.path.exists(temp_script_path):
                    os.remove(temp_script_path)
                    
            await websocket.send_text("\x1b[1;32mExecution Finished.\x1b[0m\r\n\n")
            
    except WebSocketDisconnect:
        # MAGIC LOGIC: Agar browser tab close ho jaye toh running process KILL kar do
        print("Browser tab closed by user!")
        if running_container:
            print("Killing the background process to save memory...")
            running_container.remove(force=True)
        if temp_script_path and os.path.exists(temp_script_path):
            os.remove(temp_script_path)
