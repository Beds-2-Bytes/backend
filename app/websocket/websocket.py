from typing import Dict, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, HTTPException
from .auth import verify_jwt_token_ws  # expects a raw token string

router = APIRouter()


class RoomManager:
    """
    Manages all rooms and connections.
    """
    def __init__(self):
        # rooms[room_id] = { user_id: WebSocket, ... }
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        await websocket.accept()

        if room_id not in self.rooms:
            self.rooms[room_id] = {}

        self.rooms[room_id][user_id] = websocket
        print(f"{user_id} joined room {room_id} ({len(self.rooms[room_id])} users)")

    def disconnect(self, websocket: WebSocket, room_id: str, user_id: str):
        room = self.rooms.get(room_id)
        if not room:
            return

        # Only delete if this exact socket is the one stored
        if user_id in room and room[user_id] is websocket:
            del room[user_id]
            print(f"{user_id} left room {room_id}")

        # Cleanup if room is empty
        if not room:
            del self.rooms[room_id]
            print(f"Room {room_id} deleted (no users left)")

    async def handle_message(self, room_id: str, user_id: str, message: Dict[str, Any]):
        """
        Handle an incoming JSON object from a user in a room
        and broadcast it to all other users in that same room.

        Expected client payload:
            {
              "type": "update",
              "payload": { "id": "pulse", "value": 97 }
            }
        """
        room = self.rooms.get(room_id)
        if not room:
            return

        broadcast_data = {
            "type": message.get("type", "update"),
            "from": user_id,
            "room": room_id,
            "payload": message.get("payload", message),
        }

        await self.broadcast_to_room(room_id, broadcast_data, exclude_user_id=user_id)

    async def broadcast_to_room(
        self,
        room_id: str,
        data: Dict[str, Any],
        exclude_user_id: Optional[str] = None,
    ):
        room = self.rooms.get(room_id)
        if not room:
            return

        for uid, ws in list(room.items()):
            if exclude_user_id is not None and uid == exclude_user_id:
                continue

            try:
                print("DATA: \n", data)
                await ws.send_json(data)
            except Exception as e:
                print(f"Failed to send to {uid} in room {room_id}: {e}")


manager = RoomManager()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None),
    room: str = Query(None),
):
    print("Incoming WS handshake",
          "has_token=", bool(token),
          "room=", room)

    if not token or not room:
        print("Missing token or room in WS")
        await websocket.close(code=1008)  # Policy violation
        return

    try:
        payload = verify_jwt_token_ws(token)  # must take raw string token
        user_id = payload["sub"]
        print(f"WS auth OK for user={user_id}, room={room}")
    except HTTPException as e:
        print(f"WS auth failed: {e.status_code} {e.detail}")
        await websocket.close(code=1008)
        return
    except Exception as e:
        print(f"WS unexpected error: {e}")
        await websocket.close(code=1011)
        return

    await manager.connect(websocket, room, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.handle_message(room, user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room, user_id)