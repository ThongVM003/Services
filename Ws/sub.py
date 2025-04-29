import asyncio
import websockets
from rich import print, print_json
import json


async def consume():
    uri = "ws://180.148.0.215:8001/events"
    async for websocket in websockets.connect(uri):
        try:
            print("Connected to the server")
            while True:
                message = await websocket.recv()
                print(message)
        except websockets.ConnectionClosed:
            print("Connection closed")
            continue


asyncio.get_event_loop().run_until_complete(consume())
