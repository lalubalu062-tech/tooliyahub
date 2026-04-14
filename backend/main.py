from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import docker

app = FastAPI(title="Tooliyahub API")

# VPS ke main Docker system se connect karne ke liye
try:
    docker_client = docker.from_env()
except Exception as e:
    print(f"Docker connect error: {e}")

@app.get("/")
async def read_root():
    return {"status": "Tooliyahub Backend Engine is Live!"}

# Ye wo WebSocket hai jo Terminal browser tab se connect hoga
@app.websocket("/ws/run")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Tooliyahub Terminal Connected...\r\n")
    try:
        while True:
            # User se code receive karega
            data = await websocket.receive_text()
            await websocket.send_text(f"Executing...\r\n")
            
            # (Yahan hum aage sandbox container run karne ka logic dalenge)
            await websocket.send_text(f"Code Received: {data}\r\n")
            
    except WebSocketDisconnect:
        # Browser tab band hote hi ye trigger hoga
        print("Tab closed! Process will be killed here.")
