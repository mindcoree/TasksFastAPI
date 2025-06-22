from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import uvicorn

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self,websocket:WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message:str,websocket:WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        await manager.broadcast("Клиент подключился!!!")

        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f" Сообщение:{data}")
            await manager.send_personal_message(f"Вы отправили:{data}",websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Клиент отключился!!")


if __name__ == "__main__":
    uvicorn.run("main:app")



